<script>
export default {}
</script>

<template>
  <div class="card">
    <slot name="img"></slot>
    <div class="card-body">
      <h4 class="card-title">
        <slot name="title">Dummy title</slot>
      </h4>
      <div class="card-text">
        <slot name="text">Dummy text</slot>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
