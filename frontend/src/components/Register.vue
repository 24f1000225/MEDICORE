<template>

  <div class="container mt-5">

    <div class="card p-4">

      <h2 class="text-center mb-4">Patient Registration</h2>

      <form @submit.prevent="register">

        <input
          v-model="username"
          class="form-control mb-3"
          placeholder="Username"
        />

        <input
          v-model="email"
          class="form-control mb-3"
          placeholder="Email"
        />

        <input
          v-model="password"
          type="password"
          class="form-control mb-3"
          placeholder="Password"
        />

        <button
          type="submit"
          class="btn btn-primary w-100"
        >
          Register
        </button>

      </form>

      <p class="text-center mt-3">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>

    </div>

  </div>

</template>


<script>

import API from "../services/api"

export default {

  data() {
    return {
      username: "",
      email: "",
      password: ""
    }
  },

  methods: {

    async register() {

      try {

        await API.post("/auth/register/patient", {
          username: this.username,
          email: this.email,
          password: this.password
        })

        alert("Registration successful")

        this.$router.push("/login")

      } catch (error) {

        console.error(error)

        alert("Registration failed")

      }

    }

  }

}

</script>