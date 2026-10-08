require "test_helper"

class CardDuplicateFeatureTest < ActionDispatch::IntegrationTest
  setup do
    sign_in_as :kevin
    Current.set(session: sessions(:kevin)) do
    @source = cards(:logo)
    @source.update!(title: "Reusable release checklist", description: "Confirm exports\nNotify support")
    @source.comments.create!(creator: users(:kevin), body: "Keep this discussion on the original")
    @source.reactions.create!(content: "👍", reacter: users(:david))
    @source.steps.create!(content: "Review the release notes")
    @source.assignments.create!(assignee: users(:david), assigner: users(:kevin))
    @source.toggle_tag_with("release")
    @source.pin_by(users(:david))
    @source.watch_by(users(:david))
    @source.close(user: users(:kevin))
    end
  end

  test "duplicates public card content but starts with fresh workflow state" do
    source_snapshot = [
      @source.title, @source.description.to_plain_text,
      @source.comments.pluck(:id).sort, @source.reactions.pluck(:id).sort,
      @source.steps.pluck(:id).sort, @source.assignees.pluck(:id).sort,
      @source.tags.pluck(:id).sort, @source.pins.pluck(:id).sort,
      @source.watches.pluck(:id).sort, @source.image.attached?, @source.closed?
    ]

    post "/#{@source.account.external_account_id}/cards/#{@source.number}/duplicate.json", as: :json

    assert_response :created
    json = @response.parsed_body
    assert_equal [ "description", "id", "title" ], json.keys.sort
    assert_equal "Reusable release checklist", json["title"]
    assert_equal "Confirm exports\nNotify support", json["description"]

    copy = @source.board.cards.find_by!(number: json["id"])
    assert_equal [
      copy.number,
      "Reusable release checklist",
      "Confirm exports\nNotify support"
    ], [ json["id"], json["title"], json["description"] ]
    assert_equal @source.board_id, copy.board_id
    assert_equal users(:kevin).id, copy.creator_id
    assert_not copy.closed?
    assert_empty copy.comments
    assert_empty copy.reactions
    assert_empty copy.steps
    assert_empty copy.assignees
    assert_empty copy.tags
    assert_empty copy.pins
    assert_not copy.image.attached?
    assert_equal [[ users(:kevin).id, true ]], copy.watches.pluck(:user_id, :watching)
    @source.reload
    assert_equal source_snapshot, [
      @source.title, @source.description.to_plain_text,
      @source.comments.pluck(:id).sort, @source.reactions.pluck(:id).sort,
      @source.steps.pluck(:id).sort, @source.assignees.pluck(:id).sort,
      @source.tags.pluck(:id).sort, @source.pins.pluck(:id).sort,
      @source.watches.pluck(:id).sort, @source.image.attached?, @source.closed?
    ]
  end

  test "an inaccessible source card is not duplicated" do
    private_card = Current.set(session: sessions(:kevin)) do
      boards(:private).cards.create!(title: "Private note", creator: users(:kevin), status: "published")
    end
    logout_and_sign_in_as :david

    post "/#{private_card.account.external_account_id}/cards/#{private_card.number}/duplicate.json", as: :json

    assert_response :not_found
    assert_equal 0, boards(:private).cards.where(title: "Private note").count - 1
  end
end
