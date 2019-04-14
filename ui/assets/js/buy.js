var crowdsaleContract = blankTkenContract = stableTokenContract = null;
var enoughFund = false;

$('.just-number').keypress(function(eve) {
  if ((eve.which != 46 || $(this).val().indexOf('.') != -1) && (eve.which < 48 || eve.which > 57) || (eve.which == 46 && $(this).caret().start == 0)) {
    eve.preventDefault();
  }

  $('.just-number').keyup(function(eve) {
    if ($(this).val().indexOf('.') == 0) {
      $(this).val($(this).val().substring(1));
    }
  });
});

function clearInputs() {
  $('#bdt').val('');
  $('#dai').val('');
  $('#ref').val('');
}


function updateBDTamount() {
  let rpcUrl = "https://mainnet.infura.io/v3/81a17a01107e4ac9bf8a556da267ae2d";
  var InfuraWeb3 = new Web3(new Web3.providers.HttpProvider(rpcUrl));
  var crowdsale_contract_ = InfuraWeb3.eth.contract(abiCrowdsale)
  let crowdsaleContract_ = crowdsale_contract_.at(crowdsaleAddress);

  var blank_token_contract_ = InfuraWeb3.eth.contract(abiBlankToken)
  let blankTkenContract_ = blank_token_contract_.at(blankTokenAddress);

    blankTkenContract_.balanceOf(crowdsaleAddress, function(error, result) {
      if (error) {
        return;
      }
      var r1 = result.c[0];
      blankTkenContract_.balanceOf('0x21C3cb98F203Ec5332BFDD26C806DB2b3D0fF318', function(error2, result2) {
        if (error) {
          return;
        }
        $('#av-token').html(parseInt((result2.c[0] + r1) / 10000000));
      });
    });

    blankTkenContract_.totalSupply(function(error, result) {
      if (error) {
        return;
      }
      $('#total-supply').html(parseInt(result.c[0] / 10000000));
    });
}

elementInit = function() {
  $('#msg').html('Waiting for input')
  $('#msg').css('color', 'white');
  $('.bdt-step').hide();
  $('.bdt-input').show();
  // model just exit by close btn
  $('#myModal').modal({
      backdrop: 'static',
      keyboard: false
  });
  clearInputs();
  $("#buy-btn").prop("disabled",false);
  $('.confirm-icon').hide();
  $('.loader').hide();
}

metaMaskInit = function () {
  elementInit();
  enoughFund = false;
  if (typeof web3 === 'undefined'){
    Swal.fire({
      type: 'error',
      title: 'MetaMask is not installed',
      text: 'Please install MetaMask from below link',
      footer: '<a href="https://metamask.io">Install MetaMask</a>'
    });
    return;
  }

  web3.eth.getAccounts(function(err, accounts){
    if (err != null) {
      Swal.fire({
        type: 'error',
        title: 'Something wrong',
        text: 'Check this error: ' + err,
        footer: ''
      });
    }
    else if (accounts.length === 0) {
      Swal.fire({
        type: 'info',
        title: 'MetaMask is locked',
        text: 'Please unlocked MetaMask',
        footer: ''
      });
    }
  });
    if (window.ethereum) {
      window.web3 = new Web3(ethereum);
      try {
        Web3.providers.HttpProvider.prototype.sendAsync = Web3.providers.HttpProvider.prototype.send;
        ethereum.enable();
      } catch (error) {
        console.log('User denied account access...');
        return;
      }
    }
    else if (window.web3) {
        window.web3 = new Web3(web3.currentProvider);
    }
    else {
        console.log('You should consider trying MetaMask!');
        return;
    }

    web3.eth.defaultAccount = web3.eth.accounts[0];

    var crowdsale_contract = web3.eth.contract(abiCrowdsale)
    crowdsaleContract = crowdsale_contract.at(crowdsaleAddress);

    var blank_token_contract = web3.eth.contract(abiBlankToken)
    blankTkenContract = blank_token_contract.at(blankTokenAddress);

    var stable_token_contract = web3.eth.contract(abiStableToken)
    stableTokenContract = stable_token_contract.at(stableTokenAddress);
};

function getBDTprice(coin) {
  stableTokenBalance(coin);
}

function changeActiveStep(step) {
  $('.step-box').removeClass('active');
  $('.step-box-'+step).addClass('active done');
  $('.step-box-'+step).find('.loader').show();
  $('.step-box-'+(step-1)).find('.loader').hide();
  $('.step-box-'+(step-1)).find('.confirm-icon').show();
}

function checkBalance(balance, coin) {
  crowdsaleContract.price(function(error, result) {
    if (error) {
      return;
    }
    let unitPrice = result.c[0] / 10000;
    let calAmount;
    if (coin == 'bdt') {
      let bdt = $('#bdt').val();
      if ( !bdt || parseFloat(bdt) <= 0) {
        $('#msg').css('color', 'white');
        $('#dai').val('');
        return;
      }
      calAmount = bdt * unitPrice;
      $('#dai').val(calAmount);
    }
    else {
      let dai = $('#dai').val();
      if ( !dai || parseFloat(dai) <= 0) {
        $('#msg').css('color', 'white');
        $('#bdt').val('');
        return;
      }
      calAmount = dai / unitPrice;
      $('#bdt').val(calAmount);
    }
    if ( balance < calAmount ) {
        $('#msg').css('color', 'red');
        $('#msg').html('INSUFFICIENT DAI BALANCE');
        enoughFund = false;
    }
    else {
      $('#msg').css('color', 'green');
      $('#msg').html('ENOUGH DAI BALANCE');
      enoughFund = true;
    }
  });
};

function stableTokenBalance(coin) {
  stableTokenContract.balanceOf(web3.eth.defaultAccount, function(error, result) {
    if (error) {
      return;
    }
    checkBalance(result.c[0] / 10000, coin);
  });
}


function buy() {
  if ( parseInt($('#av-token').html()) <= 0 ) {
    Swal.fire({
      type: 'error',
      title: 'NOT ENOUGH TOKEN FOR BUYING',
      text: 'Please Try Again In Next 10 Minutes',
      footer: ''
    });
    return;
  }
  val = $('#bdt').val();
  if ( val < 1  || val > 10000 ) {
    Swal.fire({
      type: 'error',
      title: 'incorect value',
      text: 'Your value should between 1 - 1000',
      footer: ''
    });
    return;
  }
  if ( !enoughFund ) {
      Swal.fire({
      type: 'error',
      title: 'Your stable coin balance is not enough',
      text: 'Please recharge your account and try again',
      footer: ''
    });
    return;
  }
  // if ( !web3.isAddress($('#ref').val()) ) {
  //   Swal.fire({
  //     type: 'error',
  //     title: 'reffere is not correct',
  //     text: 'Your reffere address is not valid, please enter an ethereum valid address',
  //     footer: ''
  //   });
  //   return;
  // }

  $('.bdt-input').hide();
  $('.bdt-step').show();
  changeActiveStep(1);

  let dei = parseFloat($('#dai').val()) * 10**18;
  stableTokenContract.approve.sendTransaction(crowdsaleAddress, dei, function(error, result) {
    if (error) {
      console.log(error);
      Swal.fire({
        type: 'error',
        title: 'Something wrong',
        text: 'Error message: ' + String(error),
        footer: ''
      });
      return;
    }
    checkApproveResult(result);
  });
  $("#buy-btn").prop("disabled",true);
}


function checkBuyTX(hash) {
  changeActiveStep(4);
  web3.eth.getTransactionReceipt(hash, function(error, result) {
    if (error) {
      console.error(error);
      return;
    }
    if (result == null) {
      setTimeout(function(){
        checkBuyTX(hash);
      }, 5000);
      return;
    }
    changeActiveStep(5);
    Swal.fire(
      'Purchase Done Successfully',
      'Please Check Your Account',
      'success'
    )
});
}

Timer = (function(){
  var self = {};
  self.second = 0;
  self.counter = null;
  self.element = null;

  self.start = function(id) {
    self.element = id;
    self.second = self.minute = self.hour = 0;
    self.counter = setInterval(function(){
      self.second++;
      let minute = 0;
      let second = 0;
      if (self.second < 60) {
       second = self.second;
       minute = hour = 0;
      }
      else {
        minute = parseInt(self.second / 60);
        second = parseInt(self.second - (minute * 60));
        let hour = parseInt(self.second / 3600);
      }
      $('#'+id).html(hour + ':' + minute + ':' + second);
    }, 1000);
  }

  self.stop = function() {
    clearInterval(self.counter);
    self.second = 0;
    $('#'+self.element).html('');
  }

  return self;
})();


function checkApproveResult(hash) {
  changeActiveStep(2);
  web3.eth.getTransactionReceipt(hash, function(error, result) {
    if (error) {
      console.error(error);
      return;
    }
    if (result == null) {
      setTimeout(function(){
        checkApproveResult(hash);
      }, 5000);
      return;
    }
    changeActiveStep(3);
    // let ref = "0xd0DC4fe9528E947AE484ebBf64198fafB902E556";
    let ref = $('.ref-box').val();
    crowdsaleContract.buy.sendTransaction(ref, function(error, result) {
      if (error) {
        console.log(error);
        return;
      }
      checkBuyTX(result);
    });
  })
};
