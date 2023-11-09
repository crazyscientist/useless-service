<script>
import AboutCard from "@/components/AboutCard.vue";

export default {
  components: {AboutCard}
}
</script>

<template>
  <div class="container">
    <div class="row">
      <h1 class="col-12  text-center">About the Useless Machine</h1>
      <div class="col-12">
        <figure class="figure py-3">
          <blockquote class="blockquote mx-5 ps-2 border-start border-3">
            A useless machine or useless box is a device whose only function is to turn itself off.
            The best-known useless machines are those inspired by Marvin Minsky's design, in which
            the device's sole function is to switch itself off by operating its own "off" switch.
            Such machines were popularised commercially in the 1960s, sold as an amusing engineering
            hack, or as a joke.
          </blockquote>
          <figcaption class="blockquote-footer text-end">
            <cite title="Wikipedia">
              <a href="https://en.wikipedia.org/wiki/Useless_machine">Wikipedia: Useless machine</a>
            </cite>
          </figcaption>
        </figure>
      </div>
    </div>
    <div class="row text-center">
      <h1 class="col-12 my-3">Behind the scenes &mdash; Meet the team</h1>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card-group">
          <AboutCard>
            <template v-slot:img>
              <img src="../assets/sebastiano-piazzi-aeXIhvO3GLo-unsplash.jpg"
                   class="card-img-top"/>
            </template>
            <template v-slot:title>Announcer</template>
            <template v-slot:text>
              Informs everybody about state changes of the switch.
            </template>
          </AboutCard>
          <AboutCard>
            <template v-slot:img>
              <img src="../assets/gabriele-stravinskaite-XFH5L93BKIc-unsplash.jpg"
                   class="card-img-top"/>
            </template>
            <template v-slot:title>Observer</template>
            <template v-slot:text>
              Looks out for the switch being turned on and requests a transaction to turn off the
              switch again.
            </template>
          </AboutCard>
          <AboutCard>
            <template v-slot:img>
              <img src="../assets/microsoft-365-7mBictB_urk-unsplash.jpg"
                   class="card-img-top"/>
            </template>
            <template v-slot:title>Manager</template>
            <template v-slot:text>
              <p>Reviews the requests and compares them to the current switch state.</p>
              <p>Approves or denies the request and orders the worker to turn the switch off.</p>
            </template>
          </AboutCard>
          <AboutCard>
            <template v-slot:img>
              <img src="../assets/ahsanization-wpvEMgFV4w0-unsplash.jpg"
                   class="card-img-top"/>
            </template>
            <template v-slot:title>Worker</template>
            <template v-slot:text>
              Performs the action of turning of the switch. If no action is required, because the
              switch was turned off in the mean time, the transaction is aborted.
            </template>
          </AboutCard>
          <AboutCard>
            <template v-slot:img>
              <img src="../assets/national-cancer-institute-OHx5zVsv_gY-unsplash.jpg"
                   class="card-img-top"/>
            </template>
            <template v-slot:title>Auditor</template>
            <template v-slot:text>
              Keeps a log of transactions and all the related actions and decisions.
            </template>
          </AboutCard>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
