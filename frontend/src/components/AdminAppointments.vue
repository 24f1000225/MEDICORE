<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">All Appointments</h2>
    <table class="table table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Doctor</th>
          <th>Patient</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
          <th>Diagnosis</th>
          <th>Treatment</th>
          <th>Prescription</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appt in appointments" :key="appt.id">
          <td>{{ appt.id }}</td>
          <td>{{ appt.doctor }}</td>
          <td>{{ appt.patient }}</td>
          <td>{{ appt.date }}</td>
          <td>{{ appt.time }}</td>
          <td>{{ appt.status }}</td>
          <td>{{ appt.diagnosis || "Not added" }}</td>
          <td>{{ appt.treatment || "Not added" }}</td>
          <td>{{ appt.prescription || "Not added" }}</td>
        </tr>

        <tr v-if="appointments.length === 0">
          <td colspan="9" class="text-center">
            No appointments found
          </td>
        </tr>
      </tbody>
    </table>

    <button
      class="btn btn-secondary"
      @click="$router.push('/admin')"
    >
      Back
    </button>
  </div>
</template>

<script>
import API from "../services/api"
export default {
  data() {
    return {
      appointments: []
    }
  },

  methods: {
    async loadAppointments() {
      try {
        const res = await API.get("/admin/appointments")
        this.appointments = res.data
      }
      catch(error) {
        console.error("Failed to load appointments:", error)
      }
    }
  },

  mounted() {
    this.loadAppointments()
  }
}
</script>