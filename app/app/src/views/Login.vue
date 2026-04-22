<template>
  <div class="container">
    <form class="form">
      <h2 class="title">{{ isLogin ? '登录' : '注册' }}</h2>

      <!-- 手机号 -->
      <div class="flex-column">
        <label>手机号</label>
      </div>
      <div class="inputForm">
        <svg height="20" viewBox="0 0 32 32" width="20" xmlns="http://www.w3.org/2000/svg">
          <g id="Layer_3" data-name="Layer 3">
            <path d="m30.853 13.87a15 15 0 0 0 -29.729 4.082 15.1 15.1 0 0 0 12.876 12.918 15.6 15.6 0 0 0 2.016.13 14.85 14.85 0 0 0 7.715-2.145 1 1 0 1 0 -1.031-1.711 13.007 13.007 0 1 1 5.458-6.529 2.149 2.149 0 0 1 -4.158-.759v-10.856a1 1 0 0 0 -2 0v1.726a8 8 0 1 0 .2 10.325 4.135 4.135 0 0 0 7.83.274 15.2 15.2 0 0 0 .823-7.455zm-14.853 8.13a6 6 0 1 1 6-6 6.006 6.006 0 0 1 -6 6z"></path>
          </g>
        </svg>
        <input
          v-model="form.phone"
          type="text"
          class="input"
          placeholder="请输入手机号"
        />
      </div>

      <!-- 密码 -->
      <div class="flex-column">
        <label>密码</label>
      </div>
      <div class="inputForm">
        <svg height="20" viewBox="-64 0 512 512" width="20" xmlns="http://www.w3.org/2000/svg">
          <path d="m336 512h-288c-26.453125 0-48-21.523438-48-48v-224c0-26.476562 21.546875-48 48-48h288c26.453125 0 48 21.523438 48 48v224c0 26.476562-21.546875 48-48 48zm-288-288c-8.8125 0-16 7.167969-16 16v224c0 8.832031 7.1875 16 16 16h288c8.8125 0 16-7.167969 16-16v-224c0-8.832031-7.1875-16-16-16zm0 0"></path>
          <path d="m304 224c-8.832031 0-16-7.167969-16-16v-80c0-52.929688-43.070312-96-96-96s-96 43.070312-96 96v80c0 8.832031-7.167969 16-16 16s-16-7.167969-16-16v-80c0-70.59375 57.40625-128 128-128s128 57.40625 128 128v80c0 8.832031-7.167969 16-16 16zm0 0"></path>
        </svg>
        <input
          v-model="form.password"
          type="password"
          class="input"
          placeholder="请输入密码"
        />
      </div>

      <!-- 注册时：确认密码 -->
      <div v-if="!isLogin" class="flex-column">
        <label>确认密码</label>
      </div>
      <div v-if="!isLogin" class="inputForm">
        <svg height="20" viewBox="-64 0 512 512" width="20" xmlns="http://www.w3.org/2000/svg">
          <path d="m336 512h-288c-26.453125 0-48-21.523438-48-48v-224c0-26.476562 21.546875-48 48-48h288c26.453125 0 48 21.523438 48 48v224c0 26.476562-21.546875 48-48 48zm-288-288c-8.8125 0-16 7.167969-16 16v224c0 8.832031 7.1875 16 16 16h288c8.8125 0 16-7.167969 16-16v-224c0-8.832031-7.1875-16-16-16zm0 0"></path>
          <path d="m304 224c-8.832031 0-16-7.167969-16-16v-80c0-52.929688-43.070312-96-96-96s-96 43.070312-96 96v80c0 8.832031-7.167969 16-16 16s-16-7.167969-16-16v-80c0-70.59375 57.40625-128 128-128s128 57.40625 128 128v80c0 8.832031-7.167969 16-16 16zm0 0"></path>
        </svg>
        <input
          v-model="form.confirmPwd"
          type="password"
          class="input"
          placeholder="请再次输入密码"
        />
      </div>

      <!-- 错误提示 -->
      <div class="tips" v-if="msg">{{ msg }}</div>

      <!-- 提交按钮 -->
      <button class="button-submit" @click.prevent="submit">
        {{ isLogin ? '登录' : '注册' }}
      </button>

      <!-- 切换登录/注册 -->
      <p class="p" @click="toggleMode">
        {{ isLogin ? '没有账号？' : '已有账号？' }}
        <span class="span">{{ isLogin ? '去注册' : '去登录' }}</span>
      </p>
    </form>
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

<style scoped>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.container {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f4ff, #d9e2ff);
}

/* 表单主体 */
.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: #ffffff;
  padding: 35px;
  width: 5.5rem;
  border-radius: 20px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  color: #151717;
  margin-bottom: 10px;
}

::placeholder {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.flex-column > label {
  color: #151717;
  font-weight: 600;
  font-size: 14px;
}

/* 输入框样式 */
.inputForm {
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  height: 50px;
  display: flex;
  align-items: center;
  padding-left: 12px;
  transition: 0.2s ease-in-out;
}

.input {
  margin-left: 10px;
  border-radius: 10px;
  border: none;
  width: 85%;
  height: 100%;
}

.input:focus {
  outline: none;
}

.inputForm:focus-within {
  border: 1.5px solid #2d79f3;
}

/* 提示文字 */
.tips {
  color: #f53f3f;
  font-size: 13px;
  text-align: center;
  min-height: 18px;
}

/* 提交按钮 */
.button-submit {
  margin: 10px 0 5px 0;
  background-color: #151717;
  border: none;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  height: 50px;
  width: 100%;
  cursor: pointer;
  transition: background 0.2s;
}

.button-submit:hover {
  background-color: #252727;
}

.p {
  text-align: center;
  color: black;
  font-size: 14px;
  margin: 5px 0;
  cursor: pointer;
}

.span {
  color: #2d79f3;
  font-weight: 500;
}
</style>
