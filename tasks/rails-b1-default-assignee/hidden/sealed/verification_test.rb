require "test_helper"

class BoardDefaultAssigneeFeatureTest < ActionDispatch::IntegrationTest
  setup do
    sign_in_as :kevin
    @board = boards(:writebook)
    @default_assignee_url = "#{@board.account.slug}/boards/#{@board.id}/default_assignee.json"
  end

  test "the JSON preference can be read, set, and cleared" do
    get @default_assignee_url
    assert_response :ok
    assert_equal({ "board_id" => @board.id, "default_assignee_id" => nil }, @response.parsed_body)

    patch @default_assignee_url, params: { default_assignee_id: users(:david).id }, as: :json
    assert_response :ok
    assert_equal({ "board_id" => @board.id, "default_assignee_id" => users(:david).id }, @response.parsed_body)
    assert_equal users(:david).id, @board.reload.default_assignee_id

    patch @default_assignee_url, params: { default_assignee_id: nil }, as: :json
    assert_response :ok
    assert_equal({ "board_id" => @board.id, "default_assignee_id" => nil }, @response.parsed_body)
    assert_nil @board.reload.default_assignee_id
  end

  test "a non-member cannot become the default and the existing choice remains" do
    private_board = boards(:private)
    private_board.update!(default_assignee_id: users(:kevin).id)

    patch "#{private_board.account.slug}/boards/#{private_board.id}/default_assignee.json", params: { default_assignee_id: users(:david).id }, as: :json

    assert_response :unprocessable_entity
    assert_equal({ "error" => "default_assignee_must_be_active_board_user" }, @response.parsed_body)
    assert_equal users(:kevin).id, private_board.reload.default_assignee_id
  end

  test "an inactive person cannot become the default and the existing choice remains" do
    users(:david).deactivate
    @board.update!(default_assignee_id: users(:kevin).id)

    patch @default_assignee_url, params: { default_assignee_id: users(:david).id }, as: :json

    assert_response :unprocessable_entity
    assert_equal({ "error" => "default_assignee_must_be_active_board_user" }, @response.parsed_body)
    assert_equal users(:kevin).id, @board.reload.default_assignee_id
  end

  test "a non-administrator cannot change the preference" do
    logout_and_sign_in_as :jz

    patch @default_assignee_url, params: { default_assignee_id: users(:david).id }, as: :json

    assert_response :forbidden
    assert_nil @board.reload.default_assignee_id
  end

  test "automatic assignment is limited to JSON card creation" do
    @board.update!(default_assignee_id: users(:david).id)

    post board_cards_path(@board)

    assert response.successful? || response.redirect?, "expected successful HTML render or redirect"
    draft = @board.cards.find_by!(creator: users(:kevin), status: "drafted")
    assert_empty draft.assignees
  end

  test "JSON-created cards receive the current default and no-default boards stay unassigned" do
    @board.update!(default_assignee_id: users(:david).id)
    post board_cards_path(@board, format: :json), params: { card: { title: "Defaulted card" } }, as: :json
    assert_response :success
    assigned_card = @board.cards.find_by!(title: "Defaulted card")
    assert_equal [ users(:david).id ], assigned_card.assignees.pluck(:id)

    @board.update!(default_assignee_id: nil)
    post board_cards_path(@board, format: :json), params: { card: { title: "Unassigned card" } }, as: :json
    assert_response :success
    unassigned_card = @board.cards.find_by!(title: "Unassigned card")
    assert_empty unassigned_card.assignees
  end
end
