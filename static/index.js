function deletePost(postId) {
    if (confirm('Are you sure you want to delete this post?')) {
        document.getElementById('delete-form-' + postId).submit();
    }
}

function deleteComment(commentId) {
    if (confirm('Are you sure you want to delete this comment?')) {
        document.getElementById('delete-comment-form-' + commentId).submit();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.remove('show');
            setTimeout(function() {
                alert.remove();
            }, 150);
        }, 5000);
    });
});
