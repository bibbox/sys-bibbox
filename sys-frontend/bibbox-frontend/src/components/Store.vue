<template>
  <div style="display: flex; flex-flow: row wrap">
    <div v-for="app in this.apps.value" :key="app">
      <StoreApp :appName="app" class="storeApp" />
    </div>
  </div>
</template>

<script>
import StoreApp from "./StoreApp.vue";
import Vue from "vue";

export default {
  components: {
    StoreApp,
  },

  mounted() {
    const axios = require("axios");
    var self = this;
    axios.get("http://127.0.0.1:5000/api/v1/apps").then((response) => {
      Vue.set(self.apps, "value", response.data);
      console.log(response.data);
    });
  },

  data() {
    return {
      apps: {},
    };
  },
};
</script>

<style>
.storeApp {
  color: #555f7d;
  padding: 15px 10px 10px 10px;
  text-align: center;
  width: 150px;
  float: left;
  background: rgba(255, 255, 255, 0.75);
  box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.3);
  margin: 10px;
  font-size: 13px;
}

.storeApp:hover {
  color: white;
  background-color: #176bae !important;
  cursor: pointer;
  border-radius: 0.25rem;
}

.img {
  height: 90px;
  width: 90px;
  float: left;
  margin-bottom: 10px;
  margin: 0 0 0 20px;
}

.name {
  float: left;
  width: 100%;
  height: 70px;
  font-size: 16px;
  margin-bottom: 10px;
  border-bottom: solid 1px #176bae;
}

.name:hover {
  border-bottom: solid 1px white;
}
</style>