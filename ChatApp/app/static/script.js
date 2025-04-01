// Get all comment buttons
const showCommentButtons = document.getElementsByClassName('comment-button');

// Loop through each button
for (let i = 0; i < showCommentButtons.length; i++) {
    showCommentButtons[i].addEventListener('click', () => {
        const postId = showCommentButtons[i].getAttribute('data-post-id');
        
        // Find all comment sections related to this post (by matching post-id)
        const commentSections = document.querySelectorAll(`.comment-section[data-post-id="${postId}"]`);
        
        // Toggle the display of the comment sections
        commentSections.forEach((section) => {
            if (section.style.display === 'none' || section.style.display === '') {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    });
}
