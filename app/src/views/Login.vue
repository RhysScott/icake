<template>
  <div class="container">
    <div class="form-box">
      <h2>{{ isLogin ? '登录' : '注册' }}</h2>

      <div class="input-item">
        <label>手机号</label>
        <input
          v-model="form.phone"
          type="text"
          placeholder="请输入手机号"
        />
      </div>

      <div class="input-item">
        <label>密码</label>
        <input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
        />
      </div>

      <div v-if="!isLogin" class="input-item">
        <label>确认密码</label>
        <input
          v-model="form.confirmPwd"
          type="password"
          placeholder="请再次输入密码"
        />
      </div>

      <div class="tips" v-if="msg">{{ msg }}</div>

      <button class="btn-submit" @click="submit">
        {{ isLogin ? '登录' : '注册' }}
      </button>

      <div class="toggle-text" @click="toggleMode">
        {{ isLogin ? '没有账号？去注册' : '已有账号？去登录' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { login, register } from '@/api/user'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isLogin = ref(true)
const msg = ref('')

const form = ref({
  phone: '',
  password: '',
  confirmPwd: ''
})

function toggleMode() {
  isLogin.value = !isLogin.value
  msg.value = ''
  form.value.confirmPwd = ''
}

async function submit() {
  const { phone, password, confirmPwd } = form.value

  if (!phone || !password) {
    msg.value = '手机号和密码不能为空'
    return
  }

  if (!isLogin.value && password !== confirmPwd) {
    msg.value = '两次密码不一致'
    return
  }

  msg.value = ''

  try {
    if (isLogin.value) {
      // 登录
      const res = await login({ phone, password })
      alert('登录成功')
      localStorage.setItem('token', res.data.token)
      router.back()

    } else {
      // 注册
      await register({ phone, password })
      alert('注册成功，请登录')
      isLogin.value = true
    }
  } catch (err) {
    msg.value = err.msg || (isLogin.value ? '登录失败' : '注册失败')
    console.error(err)
  }
}
</script>

<style>
/* 1rem = 100px */
html {
  font-size: 100px;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>

<style scoped>
.container {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f4ff, #d9e2ff);
}

.form-box {
  width: 4.16rem;
  padding: 0.52rem 0.46rem;
  background: #fff;
  border-radius: 0.21rem;
  box-shadow: 0 0.12rem 0.4rem rgba(0, 0, 0, 0.08);
}

h2 {
  text-align: center;
  margin-bottom: 0.4rem;
  font-size: 0.35rem;
  font-weight: 600;
  color: #1d2129;
}

.input-item {
  margin-bottom: 0.3rem;
}

label {
  display: block;
  margin-bottom: 0.12rem;
  font-size: 0.18rem;
  color: #4e5969;
}

input {
  width: 100%;
  height: 0.55rem;
  padding: 0 0.2rem;
  border: 1px solid #e5e6eb;
  border-radius: 0.12rem;
  outline: none;
  font-size: 0.18rem;
  transition: all 0.2s;
  background: #fafbfc;
}

input:focus {
  border-color: #409eff;
  background: #fff;
  box-shadow: 0 0 0 0.06rem rgba(64, 158, 255, 0.1);
}

.tips {
  color: #f53f3f;
  font-size: 0.16rem;
  margin-bottom: 0.15rem;
  min-height: 0.2rem;
  text-align: center;
}

.btn-submit {
  width: 100%;
  height: 0.6rem;
  background: linear-gradient(135deg, #409eff, #337eff);
  color: #fff;
  font-size: 0.22rem;
  font-weight: 500;
  border: none;
  border-radius: 0.12rem;
  cursor: pointer;
  margin-bottom: 0.3rem;
  transition: all 0.2s;
}

.btn-submit:active {
  transform: scale(0.98);
  opacity: 0.9;
}

.toggle-text {
  text-align: center;
  font-size: 0.18rem;
  color: #86909c;
  cursor: pointer;
}

.toggle-text:hover {
  color: #409eff;
}
</style>
