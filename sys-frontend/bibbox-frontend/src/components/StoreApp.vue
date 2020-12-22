<template>
  <div class="card">
    <img class="img" :src="appIcon" alt="AppLogo" />
    <div class="container">
      <span class="name">{{ appInfo.short_name }}</span>
      <p>a data collection software</p>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
export default {
  props: {
    appName: String,
  },

  data() {
    return {
      appInfo: {},
      appIcon: "",
    };
  },

  methods: {
    handleClick() {
      this.$refs["my-modal"].show();
    },
  },

  mounted() {
    var urlinfo =
      "https://raw.githubusercontent.com/bibbox/" +
      this.appName +
      "/master/appinfo.json";

    this.appIcon =
      "https://raw.githubusercontent.com/bibbox/" +
      this.appName +
      "/master/icon.png";

    const axios = require("axios");
    var self = this;

    axios
      .get(urlinfo)
      .then((response) => {
        Vue.set(self, "appInfo", response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  },
};
</script>

<style>
</style>