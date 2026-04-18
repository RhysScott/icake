<template>
  <div class="profile-page">
    <!-- 用户信息卡片 -->
    <div class="user-card">
      <div class="avatar">
        <img v-if="userInfo?.avatar_url" :src="userInfo.avatar_url" alt="头像" />
        <svg v-else class="avatar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </div>

      <div class="info">
        <div class="name">{{ userInfo?.nickname || '未设置昵称' }}</div>
        <div class="phone">{{ userInfo?.phone || '未绑定手机号' }}</div>
        <div class="desc">{{ userInfo?.bio || '这个懒狗啥都没写' }}</div>
      </div>

      <div class="arrow-right">›</div>
    </div>

    <!-- 菜单列表 -->
    <div class="menu-list">
      <div class="menu-item">
        <span class="menu-text">个人资料</span>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item">
        <span class="menu-text">设置</span>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item">
        <span class="menu-text">关于我们</span>
        <span class="menu-arrow">›</span>
      </div>
    </div>

    <!-- 退出登录 -->
    <div class="menu-list logout-group">
      <div class="menu-item logout-item" @click="handleLogout">
        <span class="menu-text">退出登录</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { get_user_info } from '@/api/user'
import { useNavbar, useTabbar } from '@/stores/layout'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const navbar = useNavbar()
const tabbar = useTabbar()
const router = useRouter()
const userInfo = ref(null)

// 获取用户信息
onMounted(async () => {
  navbar.hide()
  tabbar.show()

  try {
    const res = await get_user_info()
    userInfo.value = res.data || res
  } catch (err) {
    console.error('获取用户信息失败', err)
  }
})

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('token')
  alert('已退出登录')
  router.push('/login')
}
</script>

<style lang="scss" scoped>
// 1rem = 100px
.profile-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f2f4f7;
  padding: 0.2rem;
  box-sizing: border-box;
}

.user-card {
  background: #fff;
  border-radius: 0.2rem;
  padding: 0.3rem;
  display: flex;
  align-items: center;
  margin-bottom: 0.24rem;
  box-shadow: 0 0.02rem 0.12rem rgba(0, 0, 0, 0.06);
  position: relative;
  transition: all 0.2s ease;

  &:active {
    transform: scale(0.98);
    background-color: #fafbfc;
  }

  .avatar {
    width: 0.88rem;
    height: 0.88rem;
    background: linear-gradient(135deg, #5c7aff, #72d8ff);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.24rem;
    color: white;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .avatar-icon {
      width: 0.44rem;
      height: 0.44rem;
      stroke-width: 2;
    }
  }

  .info {
    flex: 1;
  }

  .name {
    font-size: 0.32rem;
    font-weight: 600;
    color: #1d2129;
    margin-bottom: 0.04rem;
  }

  .phone {
    font-size: 0.24rem;
    color: #86909c;
    margin-bottom: 0.06rem;
  }

  .desc {
    font-size: 0.26rem;
    color: #86909c;
  }

  .arrow-right {
    font-size: 0.36rem;
    color: #c9cdd4;
    font-weight: bold;
  }
}

.menu-list {
  background: #fff;
  border-radius: 0.2rem;
  overflow: hidden;
  box-shadow: 0 0.02rem 0.12rem rgba(0, 0, 0, 0.05);
  margin-bottom: 0.24rem;

  .menu-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.3rem 0.32rem;
    font-size: 0.29rem;
    color: #1d2129;
    border-bottom: 0.01rem solid #f2f3f5;
    transition: background 0.2s;

    &:active {
      background-color: #f7f8fa;
    }

    &:last-child {
      border-bottom: none;
    }

    .menu-arrow {
      font-size: 0.32rem;
      color: #c9cdd4;
      font-weight: 500;
    }
  }
}

.logout-group .logout-item {
  justify-content: center;
  .menu-text {
    color: #f53f3f;
    font-weight: 500;
  }
}
</style>
