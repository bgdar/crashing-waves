function todoApp() {
  return {
    newTodo: "", // Variable for the new to-do input
    pesan: "", // Teks yang akan ditampilkan di elemen HTML
    todos: [],
    p_pesan: document.querySelector(".pesan p "),
    cntr_pesan: document.querySelector(".pesan"),
    Pesan(message, pesan) {
      this.pesan = message;
      this.p_pesan.className = pesan;
      this.cntr_pesan.classList.add("show");
      setTimeout(() => {
        this.cntr_pesan.classList.remove("show");
      }, 5000);
    },
    addTodo() {
      if (this.newTodo.trim() !== "") {
        // Tampilkan data di client-side
        this.todos.push(this.newTodo);
      } else if (this.newTodo.trim() == "") {
        this.Pesan("isi dulu abg da", "error");
      }
    },
    kirim() {
      console.log(this.newTodo);
      if (this.newTodo.trim() == "") {
        this.Pesan("Tolong jangan di hapus dulu agar bisa di simpan", "error");
      } else {
        fetch("/todo/add", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ todo: this.newTodo }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Gagal mengirim data ke server");
            }
            return response.json();
          })
          .then((data) => {
            this.Pesan("Data berhasil dikirim ke server", "success");
          })
          .catch((error) => {
            console.error("Error:", error);
          });
        this.newTodo = "";
      }
    },
    deleteTodoBiasa(indexTodo) {
      this.todos = this.todos.filter((todo, index) => index !== indexTodo);
      this.Pesan("berhasil di batal kan ", "success");
    },
    deleteTodoServer(id) {
      console.log("Deleting ID:", id);
      fetch(`/todo/delete/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to delete item on server");
          }
          return response.json();
        })
        .then((data) => {
          this.Pesan(`To-Do deleted successfully${data}`, "success");
        })
        .catch((error) => {
          this.Pesan(`Error : ${error}`, "error");
        });
    },
  };
}
