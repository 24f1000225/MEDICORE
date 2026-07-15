<template>

  <div class="container mt-5">

    <h2 class="text-center mb-4">
      Update Doctor Profile
    </h2>

    <div class="card p-4">
      <div class="mb-3">
        <label class="form-label">
          Username
        </label>
        <input
          v-model="doctor.username"
          class="form-control"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">
          Email
        </label>
        <input
          v-model="doctor.email"
          class="form-control"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">
          Specialization
        </label>
        <input
          v-model="doctor.specialization"
          class="form-control"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">
          Department ID
        </label>
        <input
          v-model="doctor.department_id"
          class="form-control"
        />
      </div>

      <button
        class="btn btn-primary w-100 mb-2"
        @click="updateDoctor"
      >
        Update Doctor
      </button>

      <button
        class="btn btn-secondary w-100"
        @click="goBack"
      >
        Back
      </button>
    </div>
  </div>
</template>

<script>
import API from "../services/api"
export default {
  data() {
    return {
      doctor: {
        id: "",
        username: "",
        email: "",
        specialization: "",
        department_id: ""
      }
    }
  },

  methods: {
    async loadDoctor() {
      try {
        const id = this.$route.params.id
        const res = await API.get(`/admin/doctors/${id}`)
        this.doctor = res.data
      }
      catch(error) {
        console.error("Failed to load doctor:", error)
      }
    },

    async updateDoctor() {
      try {
        await API.put(
          `/admin/doctors/${this.doctor.id}`,
          this.doctor
        )
        alert("Doctor updated successfully")
        this.$router.push("/admin")
      }
      catch(error) {
        console.error("Update failed:", error)
        alert("Update failed")
      }
    },

    goBack() {
      this.$router.push("/admin")
    }
  },

  mounted() {
    this.loadDoctor()
  }

}

</script>