function todoApp() {
  return {
    textBaru: "",
    todos: [],
    currentEditIndex: null,
    statusCentang: false,
    isShow: false,
    textEdit: "",
    addTodo() {
      if (this.textBaru.trim() !== "") {
        this.todos.push({ text: this.textBaru, completed: false });
        this.textBaru = "";
      }
    },
    editTodo(index) {
      if (this.todos[index]) {
        this.isShow = true; // Tampilkan input edit
        this.currentEditIndex = index; // Simpan indeks saat ini
        this.textEdit = this.todos[index].text; // Isi input dengan teks saat ini
      } else {
        console.log("Data not found");
      }
    },
    updateTodo(index) {
      if (this.textEdit.trim() !== "") {
        this.todos[index].text = this.textEdit; // Perbarui nilai todo
        this.isShow = false; // Sembunyikan input edit
        this.currentEditIndex = null; // Reset indeks edit
        console.log("Updated todos:", this.todos);
      }
    },
    deleteTodo(index) {
      this.todos.splice(index, 1);
      if (this.currentEditIndex === index) {
        this.isShow = false;
        this.currentEditIndex = null;
      }
      console.log("delete todos:", this.todos);
    },
    centang(index) {
      this.todos[index].completed = !this.todos[index].completed;
      console.log(this.todos);
    },
    kirim() {
      /// yg perlu di kirim adalah array < todos > object
      // nameFile yg di kirim di ambil dari username
      fetch(`/todo/todoSave`, {
        method: "POST",
        Headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          todo: this.todos,
          nameFile: document.querySelector("#name-file").textContent,
        }), // Kirim array todos ke server
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
        })
        .catch((error) => console.error("Error:", error));
    },
  };
}
