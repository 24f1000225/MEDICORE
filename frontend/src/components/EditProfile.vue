<!-- patient apni profile update kar sakta hai  -->
<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Edit Profile</h2>
    <div class="card p-4">
      <input v-model="profile.username" class="form-control mb-3" placeholder="Username"/>
      <input v-model="profile.email" class="form-control mb-3" placeholder="Email"/>

      <button class="btn btn-success w-100" @click="updateProfile">Update Profile</button>

      <button class="btn btn-secondary mt-2 w-100" @click="$router.push('/patient')">Back</button>
    </div>
  </div>
</template>



<script>
import API from "../services/api"
export default {
  data() {
    return {
      profile: {
        username: "",
        email: ""
      }
    }
  },

  methods: {
    async loadProfile() {
      const res = await API.get("/auth/me")
      this.profile = res.data
    },

    async updateProfile() {
      await API.put("/patient/profile", this.profile)
      alert("Profile updated")
      this.$router.push("/patient")
    }
  },

  mounted() {
    this.loadProfile()
  }
}
</script>