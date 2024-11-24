document.addEventListener("DOMContentLoaded", () => {
  // fungsi hapus contact
  function deleteContact(id, name) {
    //tangkap kirim ID dari tombol saat di click
    pesan = confirm(`data atas nama ${name} apakah mau di hapus`);
    if (pesan == true) {
      fetch("/delete_contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Menyatakan tipe konten data yang dikirim
        },
        body: JSON.stringify({ id: id }), // Kirim ID data ke server
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json(); // Kembalikan promise untuk data JSON
        })
        .then((data) => {
          // Tangani respons dari server
          console.log("Sukses:", data);
          alert("Data berhasil dihapus");
        })
        .catch(() => {
          alert("Terjadi kesalahan saat menghapus data");
        });
    } else {
      alert("Penghapusan dibatalkan");
    }
  }

  //bila ada tombl id yg di clic
  const btn_id = document.querySelectorAll(".btn-contact");
  const card = document.querySelector(".cardDetail");
  const blur = document.querySelector("#blur");
  btn_id.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const id = btn.getAttribute("data-id");
      //megambil detail id dari server unt mempebaharuhi tampilan
      fetch(`contact/${id}`).then((response) => {
        response.json().then((data) => {
          // kelola data yg di dapat dari server
          card.querySelector(".name").textContent = `Nama :${data[1]}`;
          card.querySelector(".phone").textContent = `No Hp : ${data[3]}`;
          card.querySelector(".email").textContent = `Email :${data[2]}`;
          //megambil detail id dari server unt mempebaharuhi tampilan
          card.style.display = "block";

          // ubah bacground body menjadi buram
          blur.style.display = "block";
          //menambah data (Atribute) ke tombol update dan delete
          document
            .querySelector(".btn-contact .update")
            .setAttribute(
              "onclick",
              `window.location.href='/contact/update/${data[0]}';`
            );
          const btndelete = document.querySelector(".btn-contact .delete");
          btndelete.addEventListener("click", () => {
            deleteContact(data[0], data[1]);
          });
        });
      });
    });
  });
  // tomnbol close card contact
  const closeButton = card.querySelector(".close");
  closeButton.addEventListener("click", () => {
    card.style.display = "none";
    blur.style.display = "none";
  });
});

// form tambah contact strat
const addContact = document.querySelector(".imgaddcontact");
const formEdit = document.querySelector(".update-contact");
// const blur = document.querySelector("#bluri");
// Fungsi untuk menutup form
function closeForm() {
  // blur.classList.remove("background-blur");
  formEdit.innerHTML = "";
}
addContact.addEventListener("click", () => {
  formEdit.innerHTML = `
  <h3>Tambah Contact</h3>
     <form action="" id="contactForm" method="POST">
      <input type="text" name="name" id="" placeholder="Masukan Nama ..." />
      <input type="email" name="email" id="" placeholder="Masukn email..." />
      <input
        type="text"
        name="phone"
        id=""
        placeholder="Masukan nomor telepone.."
      />
      <input type="text" name="age" id="" placeholder="Umur anda..." />
      <button class="add" type="submit">Add</button>
    </form>`;

  document.addEventListener("click", function handleClickOutside(event) {
    const form = document.getElementById("contactForm");
    if (form && !form.contains(event.target) && event.target !== addContact) {
      closeForm();
      // Hapus event listener setelah form ditutup
      document.removeEventListener("click", handleClickOutside);
    }
  });
});
