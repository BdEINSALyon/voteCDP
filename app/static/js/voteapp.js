var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    candidats: listes,
  },
  methods: {
    handleChange() {
      console.log('changed');
    },
    inputChanged(value) {
      this.activeNames = value;
    },
    getComponentData() {
      return {
        on: {
          change: this.handleChange,
          input: this.inputChanged
        },
        props: {
          value: this.activeNames
        }
      }
    },
  }
});

function performVote(){
    document.getElementById("id_liste_1").value=document.getElementsByClassName("list_picked")[0].textContent;
    document.getElementById("id_liste_2").value=document.getElementsByClassName("list_picked")[1].textContent;
    document.getElementById("id_liste_3").value=document.getElementsByClassName("list_picked")[2].textContent;
    document.getElementById("id_liste_4").value=document.getElementsByClassName("list_picked")[3].textContent;
    document.getElementById("id_user_uuid").value=window.location.search.split("uuid=")[1];
    document.forms["vote_form"].submit();
}

