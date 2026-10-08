require "test_helper"
require "uri"

class ColumnWipLimitsIntegrationTest < ActionDispatch::IntegrationTest
  setup do
    sign_in_as :kevin
    @board = boards(:writebook)
    @column = columns(:writebook_triage)
  end

  test "column JSON exposes nullable limits and counts only active cards" do
    patch column_json_url(@column),
      params: { column: { wip_limit: 2 } }, as: :json
    assert_response :ok
    assert_equal 2, @response.parsed_body["wip_limit"]
    assert_equal 2, @response.parsed_body["active_cards_count"]

    # The existing fixture state has two open published cards and one closed card in this column.
    draft = cards(:unfinished_thoughts)
    draft.update_columns(account_id: @column.account_id, board_id: @board.id,
      column_id: @column.id, creator_id: users(:kevin).id, number: 9000)
    postponed = Card::NotNow.create!(card: cards(:logo), user: users(:kevin))

    get column_json_url(@column), as: :json
    assert_response :ok
    assert_equal 1, @response.parsed_body["active_cards_count"]

    get columns_json_url, as: :json
    assert_response :ok
    listed = @response.parsed_body.find { |item| item["id"] == @column.id }
    assert_equal 2, listed["wip_limit"]
    assert_equal 1, listed["active_cards_count"]

    get board_path(@board)
    assert_response :ok
    assert_select "label", text: "WIP limit"
    assert_select "input[type=number][name='column[wip_limit]']"
    assert_match "WIP: 1 / 2", @response.body

    postponed.destroy!
  end

  test "limits validate and can be cleared without changing on invalid input" do
    patch column_json_url(@column),
      params: { column: { wip_limit: 3 } }, as: :json
    assert_response :ok

    patch column_json_url(@column),
      params: { column: { name: @column.name } }, as: :json
    assert_response :ok
    assert_equal 3, @response.parsed_body["wip_limit"]

    [ 0, -1, 1.5 ].each do |invalid_limit|
      patch column_json_url(@column),
        params: { column: { wip_limit: invalid_limit } }, as: :json
      assert_response :unprocessable_entity
      assert @response.parsed_body.dig("errors", "wip_limit").present?
      assert_equal 3, saved_wip_limit
    end

    get board_path(@board)
    assert_response :ok
    document = Nokogiri::HTML(@response.body)
    wip_fields = document.css('input[name="column[wip_limit]"]')
    assert_operator wip_fields.length, :>=, 1
    candidate_forms = wip_fields.filter_map do |field|
      form = field.ancestors("form").first
      form ||= document.css("form").find { |candidate| candidate["id"] == field["form"] } if field["form"]
      form
    end.uniq
    edit_form = candidate_forms.find do |form|
      name_field = form.at_css('input[name="column[name]"]')
      name_field && name_field["value"].to_s == @column.name.to_s
    end
    edit_form ||= candidate_forms.first if candidate_forms.one?
    assert_not_nil edit_form

    wip_field = edit_form.at_css('input[name="column[wip_limit]"]')
    assert_not_nil wip_field
    label = if wip_field["id"]
      document.css("label").find { |candidate| candidate["for"] == wip_field["id"] }
    end
    label ||= wip_field.ancestors("label").first
    assert_not_nil label
    assert_match(/WIP limit/i, label.text)

    form_pairs = []
    edit_form.css("input[name], textarea[name], select[name]").each do |control|
      next if control.attribute("disabled")
      field_name = control["name"]
      next if field_name.blank?
      case control.name.downcase
      when "input"
        input_type = (control["type"] || "text").downcase
        next if %w[submit button reset image file].include?(input_type)
        if %w[checkbox radio].include?(input_type) && control.attribute("checked").nil?
          next
        end
        form_pairs << [field_name, control["value"] || ""]
      when "textarea"
        form_pairs << [field_name, control.text]
      when "select"
        options = control.css("option[selected]")
        options = control.css("option").first(1) if options.empty? && control.attribute("multiple").nil?
        options.each { |option| form_pairs << [field_name, option["value"] || option.text] }
      end
    end
    submitter = edit_form.css('button[name], input[type="submit"][name]').find do |button|
      caption = button.name.downcase == "input" ? button["value"].to_s : button.text
      caption.match?(/save|update/i)
    end
    if submitter
      caption = submitter.name.downcase == "input" ? submitter["value"].to_s : submitter.text
      form_pairs << [submitter["name"], submitter["value"] || caption]
    end
    form_params = Rack::Utils.parse_nested_query(URI.encode_www_form(form_pairs))
    assert_kind_of Hash, form_params["column"]
    form_params["column"]["wip_limit"] = ""

    form_method = edit_form["method"].to_s.downcase
    form_method = "get" if form_method.empty?
    assert_includes %w[get post], form_method
    page_uri = URI.parse(request.url)
    form_uri = URI.join(request.url, edit_form["action"].to_s)
    assert_equal [page_uri.scheme, page_uri.host, page_uri.port],
      [form_uri.scheme, form_uri.host, form_uri.port]
    form_headers = {}
    if form_method != "get" && edit_form["data-turbo"] != "false"
      form_headers["Accept"] = "text/vnd.turbo-stream.html, text/html, application/xhtml+xml"
    end
    public_send(form_method, form_uri.request_uri, params: form_params, headers: form_headers)

    app_origin = [page_uri.scheme, page_uri.host, page_uri.port]
    visited_redirects = {}
    while response.redirect?
      redirect_uri = URI.join(request.url, response.location)
      assert_equal app_origin, [redirect_uri.scheme, redirect_uri.host, redirect_uri.port]
      redirect_key = redirect_uri.to_s
      assert_nil visited_redirects[redirect_key]
      visited_redirects[redirect_key] = true
      follow_redirect!
    end
    assert_response :success

    get column_json_url(@column), as: :json
    assert_response :ok
    assert_nil @response.parsed_body["wip_limit"]
    get board_path(@board)
    assert_response :ok
    assert_no_match(/WIP:/, @response.body)

    patch column_json_url(@column),
      params: { column: { wip_limit: nil } }, as: :json
    assert_response :ok
    assert_nil @response.parsed_body["wip_limit"]

    get board_path(@board)
    assert_no_match(/WIP:/, @response.body)
  end

  test "a full column rejects both public move paths without moving the card" do
    incoming = cards(:text)
    target_id = @column.id.to_s
    initial_card_state = card_json_state(incoming)

    patch column_json_url(@column),
      params: { column: { wip_limit: 2 } }, as: :json
    assert_response :ok

    post triage_json_url(incoming, @column), as: :json
    assert_response :unprocessable_entity
    assert_equal({
      "error" => "wip_limit_reached",
      "column_id" => target_id,
      "wip_limit" => 2
    }, @response.parsed_body)
    assert_equal initial_card_state, card_json_state(incoming)

    post drop_turbo_url(incoming, @column), as: :turbo_stream
    assert_response :unprocessable_entity
    assert_select "turbo-stream[action=replace][target=flash]"
    assert_match "This column has reached its WIP limit of 2.", @response.body
    assert_equal initial_card_state, card_json_state(incoming)

    # Repeating a move for a card already active in this column does not use another slot.
    post triage_json_url(cards(:logo), @column), as: :json
    assert_2xx

    # Lowering the limit does not remove existing cards; a count above the limit stays visible.
    patch column_json_url(@column),
      params: { column: { wip_limit: 1 } }, as: :json
    assert_response :ok
    assert_equal 2, @response.parsed_body["active_cards_count"]
    get board_path(@board)
    assert_match "WIP: 2 / 1", @response.body

    # Leaving a limited column is allowed, and a newly available slot can be filled.
    post triage_json_url(cards(:logo), columns(:writebook_on_hold)), as: :json
    assert_2xx
    patch column_json_url(@column),
      params: { column: { wip_limit: 2 } }, as: :json
    assert_response :ok
    post triage_json_url(incoming, @column), as: :json
    assert_2xx

    delete triage_json_url(incoming), as: :json
    assert_2xx
    patch column_json_url(@column),
      params: { column: { wip_limit: nil } }, as: :json
    assert_response :ok
    post triage_json_url(incoming, @column), as: :json
    assert_2xx
  end

  private
    def columns_json_url
      "#{@board.account.slug}/boards/#{@board.to_param}/columns.json"
    end

    def column_json_url(column)
      "#{@board.account.slug}/boards/#{@board.to_param}/columns/#{column.id}.json"
    end

    def column_html_url(column)
      "#{@board.account.slug}/boards/#{@board.to_param}/columns/#{column.id}"
    end

    def triage_json_url(card, column = nil)
      suffix = column ? "?column_id=#{column.id}" : ""
      "#{@board.account.slug}/cards/#{card.number}/triage.json#{suffix}"
    end

    def drop_turbo_url(card, column)
      "#{@board.account.slug}/columns/cards/#{card.number}/drops/column.turbo_stream?column_id=#{column.id}"
    end

    def card_json_url(card)
      "#{@board.account.slug}/cards/#{card.number}.json"
    end

    def saved_wip_limit
      get column_json_url(@column), as: :json
      assert_response :ok
      @response.parsed_body["wip_limit"]
    end

    def card_json_state(card)
      get card_json_url(card), as: :json
      assert_response :ok
      body = @response.parsed_body
      {
        "column" => body.dig("column", "id"),
        "status" => body.fetch("status"),
        "closed" => body.fetch("closed"),
        "postponed" => body.fetch("postponed")
      }
    end

    def assert_2xx
      assert_operator response.status, :>=, 200
      assert_operator response.status, :<, 300
    end
end
