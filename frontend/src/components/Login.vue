<template>
  <div class="container mt-5">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" class="form-control mb-2" placeholder="Username" />
      <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" />
      <button class="btn btn-primary">Login</button>
    </form>
  </div>

  <p class="mt-3">
    New patient?
    <router-link to="/register">Register here</router-link>
  </p>
</template>

<script>
import API from "../services/api";

export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    async login() {
      try {
        const res = await API.post("/auth/login", {
          username: this.username,
          password: this.password
        });

        localStorage.setItem(
          "token",
          res.data.token.replace(/\s+/g, "")
        );
        localStorage.setItem("role", res.data.role);

        if (res.data.role === "admin") {
          this.$router.push("/admin");
        } else if (res.data.role === "doctor") {
          this.$router.push("/doctor");
        } else {
          this.$router.push("/patient");
        }

      } catch (err) {
        alert("Invalid Credentials");
      }
    }
  }
};
</script>