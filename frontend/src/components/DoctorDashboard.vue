<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Doctor Dashboard</h2>
    <!-- AvailabilitySection -->
    <div class="card p-3 mb-4">
      <h4 class="mb-3">Set Availability</h4>
      <input
        type="date"
        v-model="availability.date"
        class="form-control mb-2"
      />

      <input
        type="time"
        v-model="availability.time"
        class="form-control mb-2"
      />

      <button
        class="btn btn-primary"
        @click="addAvailability"
      >
        Add Availability
      </button>
    </div>

    <!-- AppointmentTable -->
    <div class="card p-3 mb-4">
      <h4 class="mb-3">Upcoming Appointment</h4>
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Patient ID</th>
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

          <!-- LoadingRow -->
          <tr v-if="loading">
            <td colspan="6" class="text-center">Loading appointments...</td>
          </tr>

          <!-- AppointmentRows -->
          <tr v-for="appt in appointments" :key="appt.id">
            <td>{{ appt.id }}</td>
            <td>{{ appt.patient_id }}</td>
            <td>{{ appt.date }}</td>
            <td>{{ appt.time }}</td>

            <!-- Status -->
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
            <td>{{ appt.diagnosis || "-" }}</td>
            <td>{{ appt.treatment || "-" }}</td>
            <td>{{ appt.prescription || "-" }}</td>

            <!-- Actions -->
            <td>
              <button
                class="btn btn-success btn-sm me-2"
                @click="approveAppointment(appt.id)"
                :disabled="appt.status !== 'Booked'"
              >
                Approve
              </button>

              <button
                class="btn btn-danger btn-sm me-2"
                @click="rejectAppointment(appt.id)"
                :disabled="appt.status !== 'Booked'"
              >
                Reject
              </button>

              <button
                class="btn btn-primary btn-sm"
                @click="openTreatment(appt)"
              >
                Add Treatment
              </button>
            </td>
          </tr>

          <!-- NoData -->
          <tr v-if="appointments.length === 0 && !loading">
            <td colspan="6" class="text-center">
              No appointments found
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- TreatmentForm -->
    <div v-if="selectedAppointment" class="card p-3 mt-4">
      <h4 class="mb-3">Update Treatment</h4>
      <textarea
        v-model="treatment.diagnosis"
        placeholder="Diagnosis"
        class="form-control mb-2"
      ></textarea>

      <textarea
        v-model="treatment.treatment"
        placeholder="Treatment"
        class="form-control mb-2"
      ></textarea>

      <textarea
        v-model="treatment.prescription"
        placeholder="Prescription"
        class="form-control mb-2"
      ></textarea>
      <textarea
        v-model="treatment.doctor_notes"
        placeholder="doctor_notes"
        class="form-control mb-2"
      ></textarea>

      <button class="btn btn-success" @click="submitTreatment">
        Save Treatment
      </button>
    </div>
    <div class="card mt-4 p-3">
      <h4>Patient Medical History</h4>
      <input v-model="patientId" class="form-control" placeholder="Enter Patient ID">
      <button class="btn btn-primary mt-2" @click="getPatientHistory">View History</button>
      <table class="table table-bordered mt-3" v-if="history.length">
        <thead>
          <tr>
            <th>Date</th>
            <th>Diagnosis</th>
            <th>Treatment</th>
            <th>Prescription</th>
            <th>Doctor Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="h in history" :key="h.appointment_id">
            <td>{{ h.date }}</td>
            <td>{{ h.diagnosis }}</td>
            <td>{{ h.treatment }}</td>
            <td>{{ h.prescription }}</td>
            <td>{{ h.doctor_notes }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="card p-3 mb-4">
      <!-- Logout -->
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import API from "../services/api"
export default {
  data() {
    return {
      appointments: [],
      patientId: "",
      history: [],
      loading: false,
      availability: {
        date: "",
        time: ""
      },
      selectedAppointment: null,
      treatment: {
        diagnosis: "",
        treatment: "",
        prescription: ""
      }
    }
  },

  methods: {
    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push("/login")
    },
    openTreatment(appt) {
      this.selectedAppointment = appt
    },
    async getPatientHistory(){
      try{
        const res = await API.get(`/doctor/patient-history/${this.patientId}`)
        this.history = res.data
      }
      catch(error){
        console.error(error)
      }
    },
    async loadAppointments() {
      try {
        this.loading = true
        const res = await API.get("/doctor/appointments")
        this.appointments = res.data
      }
      catch (error) {
        console.error("Failed to load appointments:", error)
      }
      finally {
        this.loading = false
      }
    },
    async approveAppointment(id) {
      await API.put(`/doctor/appointments/${id}`, {status: "approved"})
      this.loadAppointments()
    },
    async rejectAppointment(id) {
      await API.put(`/doctor/appointments/${id}`, {status: "rejected"})
      this.loadAppointments()
    },
    async submitTreatment() {
      try {
        await API.put(
          `/doctor/treatment/${this.selectedAppointment.id}`,
          this.treatment
        )
        alert("Treatment updated")

        this.selectedAppointment = null
        this.loadAppointments()
      }
      catch (error) {
        console.error(error)
      }
    },
    async addAvailability() {
      try {
        await API.post("/doctor/availability", this.availability)
        alert("Availability added")

        this.availability.date = ""
        this.availability.time = ""
      }
      catch (error) {
        console.error(error)
      }
    }
  },

  mounted() {
    this.loadAppointments()
  }
}
</script>