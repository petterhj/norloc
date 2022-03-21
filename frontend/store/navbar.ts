import { defineStore } from "pinia";

interface MenuItem {
  page: String;
  label: String;
}

interface MenuState {
  menuItems: MenuItem[],
  subMenuItems: MenuItem[],
}

export const useMenu = defineStore('menu', {
  // state: (): MenuState => ({
  state: (): MenuState => ({
    menuItems: [
      {label: 'Produksjoner', page: 'productions'},
      {label: 'Steder', page: 'index'},
      {label: 'Folk', page: 'index'},
      {label: 'Kart', page: 'index'}
    ],
    subMenuItems: [],
  }),
  actions: {

  }
})


// export const mutations = {
//   // add(state, text) {
//   //   state.list.push({
//   //     text,
//   //     done: false
//   //   })
//   // },
//   // remove(state, { todo }) {
//   //   state.list.splice(state.list.indexOf(todo), 1)
//   // },
//   // toggle(state, todo) {
//   //   todo.done = !todo.done
//   // }
// }

// export const getters = {
//   main: state => state.state,
// }
