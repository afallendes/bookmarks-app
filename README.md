# bookmarks-app
A simple bookmarks project made with Django/DRF, jQuery and Bootstrap4.


## Backend API Description

Method | Endpoint                      | Description
---    | ---                           | ---
GET    | /api/bookmarks/               | Retrieve all bookmarks
POST   | /api/bookmarks/               | Create bookmark
GET    | /api/bookmarks/\<int:pk>/     | Retrieve specified _pk_ bookmark
PUT    | /api/bookmarks/\<int:pk>/     | Update specified _pk_ bookmark
DEL    | /api/bookmarks/\<int:pk>/     | Delete specified _pk_ bookmark
GET    | /api/bookmarks/tag/\<int:pk>/ | Retrieve all bookmarks with _pk_ tag
GET    | /api/tags/                    | Retrieve all tags
GET    | /api/tags/\<int:pk>/          | Retrieve specified _pk_ tag
PUT    | /api/tags/\<int:pk>/          | Update specified _pk_ tag
DEL    | /api/tags/\<int:pk>/          | Delete specified _pk_ tag
