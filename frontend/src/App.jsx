import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'

// Layouts
import Layout from './components/layout/Layout'
import AdminLayout from './components/admin/AdminLayout'
import UserLayout from './components/user/UserLayout'

// RSS
import RSSFeedPage from './pages/rss/RSSFeedPage'

// Public Pages
import HomePage from './pages/HomePage'
import PostPage from './pages/PostPage'
import TagPage from './pages/TagPage'
import NotFoundPage from './pages/NotFoundPage'

// User Pages
import UserLoginPage from './pages/user/UserLoginPage'
import UserRegisterPage from './pages/user/UserRegisterPage'
import UserDashboardPage from './pages/user/DashboardPage'
import MyPostsPage from './pages/user/MyPostsPage'
import UserCreatePostPage from './pages/user/CreatePostPage'
import UserEditPostPage from './pages/user/EditPostPage'
import MyCommentsPage from './pages/user/MyCommentsPage'

// Admin Pages
import LoginPage from './pages/admin/LoginPage'
import RegisterPage from './pages/admin/RegisterPage'
import DashboardPage from './pages/admin/DashboardPage'
import PostsPage from './pages/admin/PostsPage'
import CreatePostPage from './pages/admin/CreatePostPage'
import EditPostPage from './pages/admin/EditPostPage'
import CommentsPage from './pages/admin/CommentsPage'
import UsersPage from './pages/admin/UsersPage';

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* 🌍 Public Routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="blog/:slug" element={<PostPage />} />
          <Route path="tag/:slug" element={<TagPage />} />

          {/* ✅ RSS FEED PAGE */}
          <Route path="rss" element={<RSSFeedPage />} />
        </Route>

        {/* User Auth Routes */}
        <Route path="/login" element={<UserLoginPage />} />
        <Route path="/register" element={<UserRegisterPage />} />

        {/* User Protected Routes */}
        <Route path="/user" element={<UserLayout />}>
          <Route path="dashboard" element={<UserDashboardPage />} />
          <Route path="posts" element={<MyPostsPage />} />
          <Route path="posts/create" element={<UserCreatePostPage />} />
          <Route path="posts/edit/:id" element={<UserEditPostPage />} />
          <Route path="comments" element={<MyCommentsPage />} />
        </Route>

        {/* Dashboard alias */}
        <Route path="/dashboard" element={<UserLayout />}>
          <Route index element={<UserDashboardPage />} />
        </Route>

        {/* Admin Auth Routes */}
        <Route path="/admin/login" element={<LoginPage />} />
        <Route path="/admin/register" element={<RegisterPage />} />

        {/* Admin Protected Routes */}
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="posts" element={<PostsPage />} />
          <Route path="posts/create" element={<CreatePostPage />} />
          <Route path="posts/edit/:id" element={<EditPostPage />} />
          <Route path="comments" element={<CommentsPage />} />
          <Route path="users" element={<UsersPage />} /> {/* ✅ NEW */}
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
