<script>
export default {
  data() {
    return {
      choices: [],
      switches: false,
    }
  },
  async created() {
    this.switches = await this.$api.listSwitches();
    this.loaded = true;
  }
}
</script>

<template>
  <div class="container">
    <div class="row align-items-center mt-5">
      <div class="col-6 mx-auto">
        <div class="card">
          <img class="card-img-top" src="../assets/steve-johnson-U8XpuqGEO0I-unsplash.jpg"/>
          <div class="card-header text-bg-secondary">
            <h1>
              Choose a switch
            </h1>
          </div>
          <ul class="list-group shadow">
            <li class="list-group-item" v-for="choice in switches">
              <h2>
                <RouterLink :to="{name: 'switch', params: {switchName: choice}}">
                  {{ choice }}
                </RouterLink>
              </h2>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
