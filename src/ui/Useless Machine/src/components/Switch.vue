<script>
import AuditLog from "@/components/AuditLog.vue";
import Toast from "@/components/Toast.vue";

export default {
  components: {AuditLog, Toast},
  data() {
    return {
      value: "off",
      loaded: false,
      userChanged: false,
      chatLog: [],
    }
  },
  async mounted() {
    await this.getSwitchValue();
    this.userChanged = false;
    await this.$api.switchEvents({name: this.$route.params.switchName, handler: this.onMessage})
  },
  methods: {
    async getSwitchValue() {
      this.loaded = false;
      this.value = await this.$api.switchValue({name: this.$route.params.switchName});
      this.loaded = true;
    },
    async onClick() {
      this.userChanged = true;
    },
    async onMessage(message) {
      const text = await message.data.text();
      const data = JSON.parse(text);
      this.chatLog.push({
        time: new Date(data.timestamp),
        action: data.action,
        details: data.details
      });
      await this.getSwitchValue();
    }
  },
  watch: {
    async value(newValue) {
      if (this.userChanged) {
        this.loaded = false;
        const response = await this.$api.switch({name: this.$route.params.switchName, state: newValue});
        this.userChanged = false;
        this.value = response;
        this.loaded = true;
      }
    }
  }
}
</script>

<template>
  <div class="container">
    <div class="card mt-5 shadow">
      <div class="card-header text-bg-primary">
        <h1>
          {{ $route.params.switchName }}
        </h1>
      </div>
      <div class="card-body">
        <div class="container">
          <div class="row g-2">
            <div class="col-md-6 d-flex flex-column justify-content-between px-2">
              <div class="d-flex justify-content-center my-5">
                <div class="form-check form-switch" style="width: 15rem;">
                  <input class="form-check-input" type="checkbox" role="switch" id="switch"
                         v-model="value" true-value="on" false-value="off" @click="onClick">
                </div>
              </div>
              <AuditLog/>
            </div>
            <div class="col-md-6 d-flex flex-column gap-3 p-2 border" id="toast-container">
                <Toast :content="content" v-for="content in chatLog.slice().reverse()"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#switch {
  width: 15rem;
  height: 5rem;
}

#toast-container {
  overflow-y: scroll;
  max-height: 70vh;
}
</style>
