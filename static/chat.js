let currentUserId = null;
let otherUserId = null;
let lastMessageId = 0;

function initChat(userId, otherId) {
    currentUserId = userId;
    otherUserId = otherId;
    scrollToBottom();
    setInterval(checkNewMessages, 3000);
}

function scrollToBottom() {
    const container = document.getElementById('chat-messages');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

async function checkNewMessages() {
    if (!otherUserId) return;
    
    try {
        const response = await fetch(`/api/messages/${otherUserId}`);
        const messages = await response.json();
        
        if (messages.length > 0) {
            const latestId = messages[messages.length - 1].id;
            if (latestId > lastMessageId) {
                lastMessageId = latestId;
                playNotificationSound();
            }
        }
    } catch (error) {
        console.error('Error checking messages:', error);
    }
}

function playNotificationSound() {
    const audio = new Audio('/static/new_message.mp3');
    audio.play().catch(function() {});
}
