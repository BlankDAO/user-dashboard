<template type="text/x-template">
  <div>
    <h2 class="col col-12">Location</h2>
    <hr>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col col-12">
          <label for="mySelect2" style="width: 100%;font-size: 1.5em">Type Youe City Name</label>
          <select
            style="width: 100%;"
            class="js-example-basic-single js-states form-control city"
            id="mySelect2"
            v-model="city"
          ></select>
          <hr>
          <button class="btn" v-on:click="submit">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="css">
.click-me:hover {
  cursor: pointer;
}
.title-head {
  font-family: proxima-regular;
  font-size: 2em;
  text-align: center;
  margin-top: 3%;
}
.container * {
  font-family: proxima-regular;
}
.container {
  padding: 1em 3em 2em 3em;
  margin: 6em auto;
  background-color: #fff;
  border-radius: 4.2px;
  box-shadow: 0px 3px 10px 2px rgba(0, 0, 0, 0.2);
}
.modal-input-txt {
  background-color: #000;
  color: #ffffff;
  font-family: proxima-regular;
  font-size: 1em;
}
.default-account {
  font-family: proxima-regular;
  font-size: 2em;
  /* height: 50px; */
  background-color: #fff;
}
.default-account:disabled {
  background-color: #fff;
}
.btn {
  background-color: #000;
  color: #fff;
}
</style>

<script>
module.exports = {
  data: function() {
    return {
      city: null,
      lastDate: null,
      cron: null,
      cities: null,
      selectedCity: null
    };
  },
  props: [],
  methods: {
    submit() {
      if (!this.selectedCity) {
        Swal.fire({
          type: "error",
          title: "Please select your city",
          footer: ""
        });
        return;
      }
      this.$root.loader = true;
      let headers = getHeaders();
      let data = { publicKey: this.$root.publicKey, city: this.selectedCity };
      this.$http.post("/submit-city", data, headers).then(
        function(response) {
          if (!response.data.status) {
            Swal.fire({
              type: "error",
              title: response.data.msg,
              footer: ""
            });
            this.$root.loader = false;
            return;
          }
          Swal.fire({
            type: "info",
            title: "Done Successfully",
            text: "Your city submited",
            footer: "",
            onClose: this.redirect
          });
        },
        function(response) {}
      );
    },
    redirect() {
      router.push("/");
    },
    init() {
      let app = this;
      $("select.city").change(function() {
        let id = $(this)
          .children("option:selected")
          .val();
        for (let i in app.cities) {
          let city = app.cities[i];
          if (id == city.id) {
            app.selectedCity = city;
            break;
          }
        }
      });
      if (this.$root.accountInfo.data.city) {
        Swal.fire({
          type: "info",
          title: "Your city submited",
          text: "Your City: " + this.$root.accountInfo.data.city.name,
          footer: "",
          onClose: this.redirect
        });
        return;
      }
      this.$root.loader = false;
    }
  },
  mounted() {
    this.$root.isLogin();
    let app = this;
    this.init();
    $("#mySelect2").select2({
      ajax: {
        url: "http://geodb-free-service.wirefreethought.com/v1/geo/cities",
        data: function(params) {
          var query = {
            namePrefix: params.term,
            location: "",
            radius: "",
            limit: 10,
            offset: 0,
            hateoasMode: false
          };

          // Query parameters will be ?search=[term]&type=public
          return query;
        },
        processResults: function(data) {
          let newList = [];
          data = data.data;
          app.cities = data;
          for (let i in data) {
            let item = data[i];
            newList.push({
              id: item.id,
              text: item.name + ", " + item.country
            });
          }
          // Tranforms the top-level key of the response object from 'items' to 'results'
          return {
            results: newList
          };
        }
      }
    });
  }
};
</script>