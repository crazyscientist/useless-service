<script>
export default {
  data() {
    return {
      switches: []
    }
  },
  async created() {
    this.switches = await this.$api.listSwitches();
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-md bg-body-secondary">
    <div class="container-fluid">
      <a class="navbar-brand fw-bolder" href="#">Useless Machine</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
              data-bs-target="#useless-machine-nav"
              aria-controls="useless-machine-nav" aria-expanded="false"
              aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="useless-machine-nav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link active" :to="{name: 'home'}">Home</RouterLink>
          </li>
          <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
             aria-expanded="false">
            Switches
          </a>
          <ul class="dropdown-menu">
            <li v-for="switchName in switches">
              <RouterLink class="dropdown-item"
                          :to="{name: 'switch', params: {'switchName': switchName}}">
                {{ switchName }}
              </RouterLink>
            </li>
          </ul>
        </li>

        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>

</style>
