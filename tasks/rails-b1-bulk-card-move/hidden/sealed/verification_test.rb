require "test_helper"

class BulkCardMoveFeatureTest < ActionDispatch::IntegrationTest
  setup do
    sign_in_as :kevin
    @board = boards(:writebook)
    @column = columns(:writebook_review)
  end

  test "all requested cards move and response preserves request order" do
    cards = [ cards(:layout), cards(:logo) ]
    numbers = cards.map(&:number)

    post "/#{@board.account.external_account_id}/boards/#{@board.id}/cards/bulk_move.json", params: { card_numbers: numbers, column_id: @column.id }, as: :json

    assert_response :ok
    assert_equal({ "moved_card_numbers" => numbers }, @response.parsed_body)
    assert_equal [ @column.id, @column.id ], cards.map { |card| card.reload.column_id }
  end

  test "invalid card lists and invalid columns are rejected without moving anything" do
    card = cards(:logo)
    original_column_id = card.column_id

    [ [], [ card.number, card.number ], [ 0 ], [ card.number.to_s ] ].each do |invalid_numbers|
      post "/#{@board.account.external_account_id}/boards/#{@board.id}/cards/bulk_move.json", params: { card_numbers: invalid_numbers, column_id: @column.id }, as: :json
      assert_response :unprocessable_entity
      assert_equal({ "error" => "card_numbers_must_be_nonempty_unique_integers" }, @response.parsed_body)
      assert_equal original_column_id, card.reload.column_id
    end

    post "/#{@board.account.external_account_id}/boards/#{@board.id}/cards/bulk_move.json", params: { card_numbers: [ card.number ], column_id: "missing-column" }, as: :json
    assert_response :not_found
    assert_equal({ "error" => "column_not_found" }, @response.parsed_body)
    assert_equal original_column_id, card.reload.column_id
  end

  test "a column from another board is not a valid destination" do
    card = cards(:logo)
    original_column_id = card.column_id
    foreign_column = boards(:private).columns.create!(name: "Private lane", color: "var(--color-card-1)")

    post "/#{@board.account.external_account_id}/boards/#{@board.id}/cards/bulk_move.json", params: { card_numbers: [ card.number ], column_id: foreign_column.id }, as: :json

    assert_response :not_found
    assert_equal({ "error" => "column_not_found" }, @response.parsed_body)
    assert_equal original_column_id, card.reload.column_id
  end

  test "a missing card rejects the whole request" do
    card = cards(:logo)
    original_column_id = card.column_id

    post "/#{@board.account.external_account_id}/boards/#{@board.id}/cards/bulk_move.json", params: { card_numbers: [ card.number, 999999999 ], column_id: @column.id }, as: :json

    assert_response :not_found
    assert_equal({ "error" => "card_not_found" }, @response.parsed_body)
    assert_equal original_column_id, card.reload.column_id
  end

  test "a card from another board rejects the whole request" do
    card = cards(:logo)
    original_column_id = card.column_id
    other_board_card = Current.set(session: sessions(:kevin)) do
      boards(:private).cards.create!(title: "Private card", creator: users(:kevin), status: "published")
    end

    post "/#{@board.account.external_account_id}/boards/#{@board.id}/cards/bulk_move.json", params: {
      card_numbers: [ card.number, other_board_card.number ], column_id: @column.id
    }, as: :json

    assert_response :not_found
    assert_equal({ "error" => "card_not_found" }, @response.parsed_body)
    assert_equal original_column_id, card.reload.column_id
    assert_nil other_board_card.reload.column_id
  end

  test "duplicate numbers are rejected" do
    card = cards(:logo)
    original_column_id = card.column_id

    post "/#{@board.account.external_account_id}/boards/#{@board.id}/cards/bulk_move.json", params: { card_numbers: [ card.number, card.number ], column_id: @column.id }, as: :json

    assert_response :unprocessable_entity
    assert_equal({ "error" => "card_numbers_must_be_nonempty_unique_integers" }, @response.parsed_body)
    assert_equal original_column_id, card.reload.column_id
  end

end
