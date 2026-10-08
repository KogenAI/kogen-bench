require "test_helper"
require "csv"
require "uri"

class Boards::CardExportsControllerTest < ActionDispatch::IntegrationTest
  setup do
    sign_in_as :kevin
    @account = accounts("37s")
    @user = users(:kevin)
    @board = create_board("CSV Export")
  end

  test "board page links to the CSV download" do
    get board_path(@board)

    assert_response :ok
    assert_select "a", text: "Export cards (CSV)" do |links|
      page_uri = URI.parse(request.url)
      destination = URI.join(request.url, links.first["href"].to_s)
      assert_equal [page_uri.scheme, page_uri.host, page_uri.port],
        [destination.scheme, destination.host, destination.port]
      export_path = "#{@account.slug}/boards/#{@board.to_param}/card_export"
      assert_includes [export_path, "#{export_path}.csv"], destination.path
    end
  end

  test "CSV downloads all published board cards with the stated fields and ordering" do
    column = with_actor do
      @board.columns.create!(name: "Building", color: "var(--color-card-1)")
    end

    active = create_card(@board,
      title: "CSV, \"quotes\"\nand line break",
      created_at: Time.new(2025, 4, 5, 6, 7, 8, "+03:00"),
      column: column)
    closed = create_card(@board, title: "Done")
    postponed = create_card(@board, title: "Later")
    triage = create_card(@board, title: "Needs triage")
    draft = create_card(@board, title: "Unpublished", status: "drafted")

    with_actor { closed.close(user: @user) }
    with_actor { postponed.postpone(user: @user) }

    with_actor do
      first_tag = @account.tags.create!(title: "beta")
      second_tag = @account.tags.create!(title: "alpha")
      active.taggings.create!(tag: first_tag)
      active.taggings.create!(tag: second_tag)
      active.assignments.create!(assignee: users(:jz), assigner: @user)
      active.assignments.create!(assignee: users(:david), assigner: @user)
    end

    other_board = create_board("Other board")
    foreign_card = create_card(other_board, title: "Do not export")

    # An active board filter is ignored: exports always include the full board.
    get "#{@account.slug}/boards/#{@board.to_param}/card_export.csv?indexed_by=closed&page=2"

    assert_response :ok
    assert_equal "text/csv", response.media_type
    assert_equal "utf-8", response.charset
    assert_match /\battachment\b/, response.headers["Content-Disposition"]
    assert_match /filename="?board-cards\.csv"?/, response.headers["Content-Disposition"]
    assert response.body.dup.force_encoding(Encoding::UTF_8).valid_encoding?

    rows = CSV.parse(response.body)
    assert_equal [ "Number", "Title", "Status", "Assignees", "Tags", "Created At" ], rows.shift

    expected_cards = [ active, closed, postponed, triage ].sort_by(&:number)
    assert_equal expected_cards.map { |card| card.number.to_s }, rows.map(&:first)
    refute_includes rows.map(&:first), draft.number.to_s
    refute_includes rows.map(&:first), foreign_card.number.to_s

    by_number = rows.index_by(&:first)
    assert_equal active.title, by_number.fetch(active.number.to_s)[1]
    assert_equal "Building", by_number.fetch(active.number.to_s)[2]
    assert_equal "David; JZ", by_number.fetch(active.number.to_s)[3]
    assert_equal "alpha; beta", by_number.fetch(active.number.to_s)[4]
    assert_equal "2025-04-05T03:07:08Z", by_number.fetch(active.number.to_s)[5]

    assert_equal "Done", by_number.fetch(closed.number.to_s)[2]
    assert_equal "Not now", by_number.fetch(postponed.number.to_s)[2]
    assert_equal "Maybe?", by_number.fetch(triage.number.to_s)[2]
    [ closed, postponed, triage ].each do |card|
      assert_equal "", by_number.fetch(card.number.to_s)[3]
      assert_equal "", by_number.fetch(card.number.to_s)[4]
    end
  end

  test "inaccessible and cross-account boards return 404" do
    logout_and_sign_in_as :david
    private_board = boards(:private)
    get "#{@account.slug}/boards/#{private_board.to_param}/card_export.csv"
    assert_response :not_found

    logout_and_sign_in_as :kevin
    other_account_board = boards(:miltons_wish_list)
    get "#{@account.slug}/boards/#{other_account_board.to_param}/card_export.csv"
    assert_response :not_found
  end

  private
    def with_actor(&block)
      Current.set(account: @account, session: sessions(:kevin), user: @user, &block)
    end

    def create_board(name)
      with_actor { Board.create!(name: name, all_access: true) }
    end

    def create_card(board, title:, status: "published", **attributes)
      with_actor { board.cards.create!({ title: title, status: status }.merge(attributes)) }
    end
end
