<script>
export default {
  data() {
    return {
      auditlog: [],
      loading: true
    }
  },
  props: ["disabled"],
  methods: {
    async onClick() {
      this.loading = true;
      const entries = await this.$api.auditLog({name: this.$route.params.switchName});
      this.auditlog.length = 0;
      entries.forEach(entry => {
        entry.details = entry.details.map(x => {
          x.timestamp = new Date(x.timestamp);
          return x
        });
        this.auditlog.push(entry);
      });
      this.loading = false;
    }
  }
}
</script>

<template>
  <button type="button" class="btn btn-secondary" id="auditlog-button" data-bs-toggle="modal"
          data-bs-target="#auditlog-modal" @click="onClick" :disabled="disabled">
    <div class="d-flex align-items-center">
      <img class="avatar border border-2 shadow me-3"
           src="../assets/national-cancer-institute-OHx5zVsv_gY-unsplash.jpg"/>
      <span class="flex-grow-1 text-center fw-bold">Review audit log</span>
    </div>
  </button>
  <div class="modal modal-lg" id="auditlog-modal">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <img class="avatar border border-2 shadow me-3"
               src="../assets/national-cancer-institute-OHx5zVsv_gY-unsplash.jpg"/>
          <h2 class="modal-title">Audit Log</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"/>
        </div>
        <div class="modal-body">
          <template v-if="loading">
            <h4 class="placeholder-glow">
              <span class="placeholder col-8"></span>
            </h4>
            <p class="placeholder-glow">
              <span class="placeholder col-7"></span>
              <span class="placeholder col-4"></span>
              <span class="placeholder col-4"></span>
              <span class="placeholder col-6"></span>
            </p>
          </template>
          <template v-else>
            <div class="alert alert-warning" v-if="auditlog.length === 0">
              No log entries available.
            </div>
            <template v-for="entry in auditlog">
              <h4>Transaction: <span class="font-monospace text-nowrap">{{ entry.id }}</span></h4>
              <table class="table table-striped table-sm">
                <thead>
                <tr>
                  <th scope="col">Action</th>
                  <th scope="col">Timestamp</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="detail in entry.details">
                  <td>{{ detail.action }}</td>
                  <td>{{ detail.timestamp.toLocaleString() }}</td>
                </tr>
                </tbody>
              </table>
            </template>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.avatar {
  width: 4rem;
  height: 4rem;
  border-radius: 1.5rem;
}
</style>
