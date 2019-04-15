<template type="text/x-template">
  <div class="modal fade" id="myModal">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h4 class="modal-title"></h4>
          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        <!-- Modal body -->
        <div class="modal-body step-progress">
          <div class="col col-12 row justify-content-center bdt-step animated fadeIn">
            <div
              class="col col-12 row justify-content-center step-box step-box-1"
              v-for="(step, index) in steps"
              v-bind:id="step.id"
              v-bind:class="{ active: index == currentStep, done: index < currentStep }"
            >
              <div class="col col-1">
                <img src="assets/image/metamask.png" height="30" v-if="step.type == 'metamask'">
                <img src="assets/image/trx.png" height="30" v-else-if="step.type == 'trx'">
                <img :src="'assets/image/' + step.type + '.png'" height="30" v-else>
              </div>
              <div class="col col-8">
                <p class="t-text">{{step.text}}</p>
              </div>
              <div class="col col-2">
                <div class="loader" v-show="index == currentStep"></div>
                <div class="confirm-icon" v-show="index < currentStep">
                  <img src="assets/image/confirm.png" height="30">
                </div>
              </div>
              <div class="sprator"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="css">
.step-progress .loader {
  border: 5px solid #f3f3f3;
  border-radius: 50%;
  border-top: 5px solid black;
  width: 35px;
  height: 35px;
  -webkit-animation: spin 2s linear infinite; /* Safari */
  animation: spin 2s linear infinite;
}
@-webkit-keyframes spin {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.step-progress .sprator {
  border: 1px solid #e9ecef;
  width: 1200px;
  margin-bottom: 3%;
  margin-top: 1%;
}

.step-progress img {
  margin-top: 5px;
  -webkit-filter: grayscale(100%); /* Safari 6.0 - 9.0 */
  filter: grayscale(100%);
}
.step-box {
  transition: opacity 2s;
  opacity: 0.3;
}
.step-box.done {
  transition: opacity 2s;
  opacity: 1;
}
.step-box.active {
  transition: opacity 2s;
  opacity: 1;
}
.bdt-step .t-text {
  font-family: proxima-regular;
  font-size: 2vmin;
  color: grayscale;
  margin-top: 5px;
}
.bdt-step .active .t-text {
  font-family: proxima-semibold;
  font-size: 2.5vmin;
  color: black;
}
</style>

<script>
module.exports = {
  data: function() {
    return {
      steps: null,
      currentStep: 0
    };
  },
  props: ["datas"],
  methods: {
    init() {
      this.currentStep = 0;
      this.assignId();
      $("#myModal").modal({
        backdrop: "static",
        keyboard: false
      });
    },
    assignId() {
      for (var i in this.steps) {
        let id =
          "step-" +
          Math.random()
            .toString(36)
            .substring(7);
        this.steps[i].id = id;
      }
    },
    nextStep() {
      if (this.currentStep >= this.steps.length) {
        Swal.fire("Done Successfully", "", "success");
        return;
      }
      this.currentStep++;
    }
  },
  update() {},
  mounted() {
    this.steps = this.datas;
    this.init();
    this.$root.$on("nextStep", () => {
      this.nextStep();
    });
  }
};
</script>