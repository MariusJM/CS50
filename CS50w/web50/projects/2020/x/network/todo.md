# Social Network Implementation Specification

## Requirements

### Tweet model

### New Post:

- Users who are signed in can create a new text-based post by filling in text into a text area and clicking a button to submit the post.
- Optionally, implement the "New Post" box at the top of the "All Posts" page or as a separate page.

### All Posts:
- The "All Posts" link in the navigation bar leads to a page displaying all posts from all users, with the most recent posts first.
- Each post should include the username, post content, date and time of creation, and the number of "likes."

### Profile Page:
- Clicking on a username should load that user’s profile page, displaying:
  - The number of followers the user has.
  - The number of people that the user follows.
  - All posts for that user, in reverse chronological order.
  - For any other signed-in user, display a "Follow" or "Unfollow" button to toggle whether they are following this user’s posts. (Note: A user cannot follow themselves.)

### Following:
- The "Following" link in the navigation bar takes the user to a page displaying posts made by users they follow.
- This page behaves like the "All Posts" page but with a limited set of posts.
- Only available to signed-in users.

### Pagination:
- On any page displaying posts, show 10 posts per page.
- If there are more than ten posts, a "Next" button should appear to take the user to the next page of older posts.
- If not on the first page, a "Previous" button should appear to take the user to the previous page of posts.

### Edit Post:
- Users can click an "Edit" button or link on any of their own posts to edit that post.
- Clicking "Edit" replaces the post's content with a textarea for editing.
- Users can then "Save" the edited post without requiring a reload of the entire page.
- Ensure security to prevent a user from editing another user’s posts.

### "Like" and "Unlike":
- Users can click a button or link on any post to toggle whether or not they "like" that post.
- Use JavaScript to asynchronously update the server with the like count (via a fetch call) and then update the post’s like count displayed on the page without requiring a reload of the entire page.
