<script>
export default {
  props: ['content'],
  computed: {
    toastClass() {
      if (this.content.action === "changed") {
        return 'bg-secondary-subtle text-secondary';
      } else if (this.content.action === 'approved') {
        return 'text-success bg-success-subtle';
      } else if (this.content.action === 'executed') {
        return 'text-success-emphasis bg-success-subtle';
      } else if (this.content.action === 'denied') {
        return 'text-danger bg-danger-subtle';
      } else if (this.content.action === 'aborted') {
        return 'bg-warning-subtle';
      }
    },
    avatarImg() {
      if (['approved', 'denied'].includes(this.content.action)) {
        return 'manager';
      } else if (this.content.action === 'request') {
        return 'observer';
      } else if (['executed', 'aborted'].includes(this.content.action)) {
        return 'worker';
      } else if (this.content.action === 'changed') {
        return 'megaphone';
      }
    }
  }
}
</script>

<template>
  <div class="d-flex gap-2">
    <img v-if="avatarImg === 'observer'"
         src="../assets/gabriele-stravinskaite-XFH5L93BKIc-unsplash.jpg"
         class="border border-2 shadow-sm avatar"/>
    <img v-else-if="avatarImg === 'manager'"
         src="../assets/microsoft-365-7mBictB_urk-unsplash.jpg"
         class="border border-2 shadow-sm avatar"/>
    <img v-else-if="avatarImg === 'worker'"
         src="../assets/ahsanization-wpvEMgFV4w0-unsplash.jpg"
         class="border border-2 shadow-sm avatar"/>
    <img v-else-if="avatarImg === 'megaphone'"
         src="../assets/sebastiano-piazzi-aeXIhvO3GLo-unsplash.jpg"
         class="border border-2 shadow-sm avatar"/>

    <div class="toast show w-100 shadow" role="alert"
         :class="toastClass">
      <div class="toast-body">
        <p class="mb-0"><strong>{{ content.details }}</strong></p>
        <p class="text-end p-0 m-0"><small>{{ content.time.toLocaleString() }}</small></p>
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
