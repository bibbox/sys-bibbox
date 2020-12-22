<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <img class="nav" alt="logo" src="../assets/logo.png" />
      <b-navbar-brand href="#">silicolab</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-navbar-nav class="ml-auto">
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item class="co" href="#">Lab Description</b-nav-item>
            <b-nav-item href="#">Biobank</b-nav-item>
            <b-nav-item href="#">Applications</b-nav-item>
            <b-nav-item href="#">Store</b-nav-item>
            <b-nav-item href="#">Activities</b-nav-item>
            <b-nav-item href="#">Settings</b-nav-item>
            <b-avatar :size="40"></b-avatar>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
export default {};
</script>
    
<style scoped>
.navbar.navbar-dark.bg-dark {
  background-color: #176bae !important;
  font-family: "Verdana", "sans-serif";
  font-size: 18px;
}

.nav {
  height: 40px;
  width: 60px;
  padding-right: 15px;
  margin-right: 15px;
  border-right: solid 2px #ffffff;
}

.navbar-dark .navbar-nav .nav-link {
  color: #ffffff;
}

.navbar-dark .navbar-brand {
  font-family: "Verdana", "sans-serif";
  font-size: 28px;
}

.navbar-dark .navbar-nav .nav-link:hover {
    background-color: #005090;
}
</style>