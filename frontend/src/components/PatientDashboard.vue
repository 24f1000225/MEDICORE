<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Patient Dashboard</h2>
    <!-- edit profiel button -->
    <button
      class="btn btn-primary mb-3" @click="$router.push('/edit-profile')">
      Edit Profile
    </button>

    <!-- doctor search baar -->
    <div class="card mt-4 p-3">
      <h4>Search Doctor by Specialization</h4>
      <input
        v-model="specialization"
        class="form-control"
        placeholder="Enter specialization"
      >
      <button
        class="btn btn-primary mt-2"
        @click="searchDoctors"
      >
        Search
      </button>
    </div>

    <table class="table table-bordered mt-3">

      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Specialization</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="doc in doctors" :key="doc.id">

          <td>{{ doc.id }}</td>
          <td>{{ doc.username }}</td>
          <td>{{ doc.email }}</td>
          <td>{{ doc.specialization }}</td>

        </tr>

      </tbody>

    </table>


    <!-- Book Appointment -->
    <div class="card p-3 mb-4">
      <h4>Book Appointment</h4>
      <form @submit.prevent="bookAppointment">
        <!-- Doctor Select -->
        <select v-model="form.doctor_id" class="form-control mb-2" @change="loadAvailability">
          <option disabled value="">Select Doctor</option>
          <option
            v-for="doc in doctors"
            :key="doc.id"
            :value="doc.id"
          >
            {{ doc.username }} ({{ doc.specialization }})
          </option>
        </select>

        <!-- Available Slots -->

        <select v-model="selectedSlot" class="form-control mb-2">
          <option disabled value="">Select Available Slot</option>

          <option
            v-for="slot in availability"
            :key="slot.date + slot.time"
            :value="slot"
          >

            {{ slot.date }} - {{ slot.time }}

          </option>
        </select>

        <button class="btn btn-primary">Book Appointment</button>
      </form>
    </div>



    <!-- My Appointments -->

    <div class="card p-3">
      <h4>My Appointments</h4>
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Doctor</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Diagnosis</th>
            <th>Treatment</th>
            <th>Prescription</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="appt in appointments"
            :key="appt.id"
          >
            <td>{{ appt.id }}</td>
            <td>{{ appt.doctor_name }}</td>
            <td>{{ appt.date }}</td>
            <td>{{ appt.time }}</td>

            <td>
              <span
                :class="{
                  'text-warning': appt.status === 'pending',
                  'text-success': appt.status === 'approved',
                  'text-danger': appt.status === 'rejected'
                }"
              >
                {{ appt.status }}
              </span>
            </td>

            <td>{{ appt.diagnosis || "Not updated" }}</td>
            <td>{{ appt.treatment || "Not updated" }}</td>
            <td>{{ appt.prescription || "Not updated" }}</td>

            <td>
              <button class="btn btn-danger btn-sm" @click="cancelAppointment(appt.id)">Cancel</button>
            </td>
          </tr>

          <tr v-if="appointments.length === 0">
            <td colspan="6" class="text-center">No appointments found</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Past Appointment History -->

    <div class="card p-3 mt-4">
      <h4>Past Appointment History</h4>
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
          <th>ID</th>
          <th>Doctor</th>
          <th>Date</th>
          <th>Diagnosis</th>
          <th>Treatment</th>
          <th>Prescription</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="h in history" :key="h.id">
            <td>{{ h.id }}</td>
            <td>{{ h.doctor_id }}</td>
            <td>{{ h.date }}</td>
            <td>{{ h.diagnosis || "Not updated" }}</td>
            <td>{{ h.treatment || "Not updated" }}</td>
            <td>{{ h.prescription || "Not updated" }}</td>
          </tr>
        <tr v-if="history.length === 0">
          <td colspan="6" class="text-center">No past records</td>
        </tr>
        </tbody>
      </table>
      <button class="btn btn-danger" @click="logout">Logout</button>
      <button class="btn btn-success mt-3" @click="exportCSV">Export Treatment History (CSV)</button>
    </div>
  </div>
</template>


<script>
import API from "../services/api"
export default {
  data() {
    return {
      doctors: [],
      appointments: [],
      specialization: "",
      availability: [],
      history:[],
      selectedSlot: "",

      form: {
        doctor_id: ""
      }
    }
  },

  methods: {

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push("/login")
    },
    async exportCSV(){
      try{
        await API.post("/patient/export")
        alert("Export started. CSV will be generated soon.")
      }
      catch(error){
        console.error(error)
      }
    },
    async searchDoctors(){
      try{
        const res = await API.get(`/patient/doctors?specialization=${this.specialization}`)
        this.doctors = res.data
      }
      catch(error){
        console.error(error)
      }
    },
    async loadProfile(){
      const res = await API.get("/auth/me")
      this.profile = res.data
    },
    async loadHistory(){
      const res = await API.get("/patient/history")
      this.history = res.data
    },
    async loadAppointments() {
      const res = await API.get("/patient/appointments")
      this.appointments = res.data
    },
    async loadDoctors() {
      const res = await API.get("/admin/doctors")
      this.doctors = res.data
    },
    async loadAvailability() {
      try {

        const res = await API.get(
          `/patient/doctor-availability/${this.form.doctor_id}`
        )

        this.availability = res.data
      }
      catch (error) {

        console.error(error)
      }
    },
    async bookAppointment() {

      try {

        await API.post("/patient/book", {

          doctor_id: this.form.doctor_id,

          date: this.selectedSlot.date,

          time: this.selectedSlot.time

        })

        alert("Appointment booked successfully")

        this.loadAppointments()

      }

      catch (error) {

        console.error(error)

      }

    },
    async cancelAppointment(id) {

      await API.delete(`/patient/appointments/${id}`)

      this.loadAppointments()

    }
  },

  mounted() {
    this.loadDoctors()
    this.loadAppointments()
    this.loadHistory()
  }
}

</script>