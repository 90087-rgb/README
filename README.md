# Social App

A simple social media application built with Flask.

## Features

- User authentication (login, signup, logout)
- Create, view, and delete posts
- Like posts
- Comment on posts
- Follow/unfollow users
- Real-time chat messaging
- Notifications
- User profiles
- Search for users and posts

## Project Structure

```
proyecto/
├── instance/
├── static/
│   ├── uploads/
│   ├── chat.js
│   ├── index.js
│   ├── styles.css
│   ├── notification.mp3
│   └── new_message.mp3
├── website/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── views.py
│   ├── social.py
│   ├── utils/
│   │   └── search_algorithms.py
│   ├── structures/
│   │   ├── heap.py
│   │   ├── queue.py
│   │   ├── hashset.py
│   │   ├── linkedlist_posts.py
│   │   ├── comment_list.py
│   │   └── graph_follow.py
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── sign_up.html
│       ├── posts.html
│       ├── notifications.html
│       ├── social_people.html
│       ├── social_profile.html
│       ├── chat.html
│       ├── chats_list.html
│       └── search_results.html
├── main.py
├── README.md
└── requirements.txt
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Open http://localhost:5000 in your browser

## Data Structures Used

- **MaxHeap**: For sorting posts by score
- **Queue**: For message queuing
- **HashSet**: For efficient lookups
- **LinkedListPosts**: For managing posts
- **CommentList**: For managing comments
- **FollowGraph**: For managing follow relationships

## Search Algorithms

- **Boyer-Moore**: Fast string search algorithm
- **KMP**: Knuth-Morris-Pratt string search algorithm