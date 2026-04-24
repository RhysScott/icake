import { defineStore } from 'pinia';
import { ref } from 'vue';

/**
 * Tabbar（底部标签栏）状态管理
 */
export const useTabbar = defineStore('tabbar', () => {
    // 控制 Tabbar 是否显示，默认显示
    const visible = ref(true);

    /**
     * 显示 Tabbar
     */
    const show = () => visible.value = true;

    /**
     * 隐藏 Tabbar
     */
    const hide = () => visible.value = false;

    /**
     * 切换 Tabbar 显示状态
     * true -> false 或 false -> true
     */
    const toggle = () => visible.value = !visible.value;

    // 暴露状态和方法
    return {
        visible, // 当前显示状态
        show,    // 显示方法
        hide,    // 隐藏方法
        toggle   // 切换方法
    };
});


/**
 * Navbar（顶部导航栏）状态管理
 */
export const useNavbar = defineStore('navbar', () => {
  // 控制 Navbar 是否显示，默认显示
  const visible = ref(true);
  const title = ref('标题');

  /**
   * 显示 Navbar
   */
  const show = () => visible.value = true;

  /**
   * 隐藏 Navbar
   */
  const hide = () => visible.value = false;

  /**
   * 切换 Navbar 显示状态
   */
  const toggle = () => visible.value = !visible.value;

  /**
   * 设置 Navbar 标题
   */
  const setTitle = newTitle => title.value = newTitle;

  /**
   * 获取 Navbar 标题
   */

  const getTitle = () => title.value;

  // 暴露状态和方法
  return {
    visible, // 当前显示状态
    show,    // 显示方法
    hide,    // 隐藏方法
    toggle,   // 切换方法
    title,  // 当前标题
    setTitle, // 设置标题
    getTitle // 获取标题
  };
});
