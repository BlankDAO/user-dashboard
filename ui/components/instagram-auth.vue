<template type="text/x-template">
    <div class="">
      <div class="row justify-content-center">
	      <h2 class="col col-12">Instagram</h2>
	      <hr>
          <div class="col col-12">
            <div class="input-group input-group-icon col col-12">
              <div class="input-group-prepend">
                <span class="input-group-text modal-input-txt">Instagram Username</span>
              </div>
              <input type="text" @keyup.enter="submit" v-model="username" class="form-control" placeholder="Your Instagram Username">
            </div>
          </div>
          <div class="col col-12">
            <button class="btn" v-on:click="submit">
               <i class="fa fa-arrow-alt-circle-right"></i> Submit
            </button>
          </div>
      </div>
    </div>

</template>

<style lang="css">
.input-group {
  margin-top: 20px;
  margin-bottom: 20px;
}
.modal-input-txt {
  background-color: #000;
  color: #ffffff;
  font-family: proxima-regular;
  font-size: 1.2em;
}
.form-control {
  font-family: proxima-regular;
  font-size: 1.5em;
}
.btn {
  font-family: proxima-regular;
  font-size: 16px;
  margin-top: 2vmin;
  margin-left: 2vmin;
  color: #111A44;
  width: 200px;
  height: auto;
  border-color: #111A44;
  background-color: white;
}
.btn i {
  float: left;
  margin-top: 5px;
}
</style>

<script>
  module.exports = {
    data: function() {
      return {
        username: '',
      }
    },
    props: [
    ],
    methods: {
      submit() {
        if( this.username.length < 1 ) {
          Swal.fire({
            type: 'error',
            title: "Username can't be empty",
            text: "Please enter your instagram username",
            footer: ''
          });
          return;
        }
        let data = {
          'publicKey': this.$root.accountInfo.data.publicKey,
          'instagram_username': this.username,
        };
        this.$http.post('/submit-instagram', data).then(function(response){
          let data = response.data;
          if ( !data.status ) {
            Swal.fire({
              type: 'error',
              title: 'Error on saving data',
              text: 'Details: ' + data.msg,
              footer: ''
            });
            return;
          }
          Swal.fire(
            'Done Successfully',
            data.msg,
            'success'
          );
          router.push('/');
        },function(response){
          console.error('Error in Connection: ', response)
        });
      },
    },
    mounted(){
      if ( this.$root.accountInfo.data.instagram_confirmation === true ) {
          Swal.fire(
            'Already done',
            'Your instagram username submited',
            'info'
          );
          router.push('/');
      }
    }
  }
</script>

