require "uri"
require "test_helper"

class RailsB1CardDueDatesTest < ActionDispatch::IntegrationTest
  setup do
    sign_in_as :kevin
  end

  test "JSON create persists and returns a due date" do
    date = "2032-12-17"

    post board_cards_path(boards(:writebook)),
      params: { card: { title: "Prepare release notes", due_on: date } },
      as: :json

    assert_response :success
    assert_equal date, response.parsed_body.fetch("due_on")

    get card_path(response.parsed_body.fetch("number")), as: :json

    assert_response :success
    assert_equal date, response.parsed_body.fetch("due_on")
  end

  test "JSON update preserves omitted values and clears null or blank values" do
    card = cards(:logo)
    date = "2032-12-17"

    patch card_path(card), params: { card: { due_on: date } }, as: :json
    assert_response :success
    assert_equal Date.iso8601(date), card.reload.due_on

    patch card_path(card), params: { card: { title: "Updated title" } }, as: :json
    assert_response :success
    assert_equal Date.iso8601(date), card.reload.due_on

    patch card_path(card), params: { card: { due_on: "" } }, as: :json
    assert_response :success
    assert_nil card.reload.due_on

    patch card_path(card), params: { card: { due_on: date } }, as: :json
    assert_response :success
    patch card_path(card), params: { card: { due_on: nil } }, as: :json
    assert_response :success
    assert_nil card.reload.due_on
  end

  test "single-card and list JSON include a date or null" do
    card = cards(:logo)
    card.update!(due_on: Date.new(2032, 12, 17))

    get card_path(card), as: :json
    assert_response :success
    assert_equal "2032-12-17", response.parsed_body.fetch("due_on")

    get cards_path, as: :json
    assert_response :success
    cards = response.parsed_body.index_by { |item| item.fetch("number") }
    assert_equal "2032-12-17", cards.fetch(card.number).fetch("due_on")
    assert_nil cards.fetch(cards(:layout).number).fetch("due_on")
  end

  test "both HTML editors expose the due date input" do
    date = Date.new(2032, 12, 17)
    card = cards(:logo)
    card.update!(due_on: date)

    get edit_card_path(card)
    assert_response :success
    assert_select "label", text: "Due date"
    assert_select "input[type='date'][name='card[due_on]'][value='2032-12-17']"

    draft = boards(:writebook).cards.create!(creator: users(:kevin), status: "drafted")
    get card_draft_path(draft)
    assert_response :success
    assert_select "label", text: "Due date"
    assert_select "input[type='date'][name='card[due_on]']"
  end

  test "HTML editor forms persist and clear the date through their rendered actions" do
    date = "2032-12-17"
    published = cards(:logo)
    published.update!(due_on: nil)
    draft = boards(:writebook).cards.create!(creator: users(:kevin), status: "drafted")

    [[edit_card_path(published), published, true], [card_draft_path(draft), draft, false]].each do |editor_path, card, public_detail_json|
      submit_due_date_form(editor_path, date)
      assert_equal date, persisted_due_on(card, public_detail_json: public_detail_json)

      submit_due_date_form(editor_path, "")
      assert_nil persisted_due_on(card, public_detail_json: public_detail_json)
    end
  end

  test "preview and detail display a due date, while detail omits an unset due date" do
    card = cards(:logo)
    card.update!(due_on: Date.new(2032, 12, 17))

    get cards_path
    assert_response :success
    assert_select "time[datetime='2032-12-17']", text: "Due 2032-12-17"

    get card_path(card)
    assert_response :success
    assert_select "time[datetime='2032-12-17']", text: "Due 2032-12-17"

    unset_card = cards(:layout)
    unset_card.update!(due_on: nil)
    get card_path(unset_card)
    assert_response :success
    assert_select "time" do |time_elements|
      assert time_elements.none? { |element| element.text.start_with?("Due ") }
    end
  end
  private

  def submit_due_date_form(editor_path, due_on)
    get editor_path
    assert_response :success

    input = css_select("input[type='date'][name='card[due_on]']").first
    assert input, "the editor page must expose a due-date input"
    form = if input["form"].present?
      css_select("form").find { |candidate| candidate["id"] == input["form"] }
    else
      input.xpath("ancestor::form[1]").first
    end
    assert form, "the due-date input must belong to a form"

    action = form["action"].presence || request.fullpath
    target = URI.join(request.url, action)
    assert_equal request.host, target.host if target.host
    browser_method = (form["method"].presence || "get").downcase
    method_override = form.at_css("input[name='_method']")&.[]("value")&.downcase
    params = { card: { due_on: due_on } }

    assert_includes %w[get post], browser_method
    if browser_method == "post"
      params[:_method] = method_override if method_override.present?
      post target.request_uri, params: params
    else
      get target.request_uri, params: params
    end
  end

  def persisted_due_on(card, public_detail_json:)
    if public_detail_json
      get card_path(card), as: :json
      assert_response :success
      response.parsed_body.fetch("due_on")
    else
      card.reload.due_on&.iso8601
    end
  end

end
