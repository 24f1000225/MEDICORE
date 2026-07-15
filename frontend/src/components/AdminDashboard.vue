<template>
  <div class="container mt-4">

    <h2>Admin Dashboard</h2>
    
    <!-- admin Dashboard  -->
    <div class="row mt-3">
      <div class="col-md-4">
        <div class="card p-3 text-center">
          <h5>Total Doctors</h5>
          <h3>{{ stats.total_doctors }}</h3>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card p-3 text-center">
          <h5>Total Patients</h5>
          <h3>{{ stats.total_patients }}</h3>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card p-3 text-center">
          <h5>Total Appointments</h5>
          <h3>{{ stats.total_appointments }}</h3>
          <button class="btn btn-primary mb-3" @click="$router.push('/admin/appointments')">
            View All Appointments
          </button>
        </div>
      </div>
    </div>
    
    <div class="card mt-4 p-3">
    
      <h4>Search</h4>
    
      <div class="row">
    
        <div class="col-md-6">
    
          <input
            v-model="searchDoctor"
            class="form-control"
            placeholder="Search Doctor"
          >
    
          <button
            class="btn btn-primary mt-2"
            @click="searchDoctors"
          >
            Search Doctor
          </button>
    
        </div>
    
        <div class="col-md-6">
    
          <input
            v-model="searchPatient"
            class="form-control"
            placeholder="Search Patient"
          >
    
          <button
            class="btn btn-primary mt-2"
            @click="searchPatients"
          >
            Search Patient
          </button>
    
        </div>
    
      </div>
    
    </div>
    
    <!-- doctors table -->
    <h4>Doctors</h4>
    
    <table class="table table-bordered">
      <thead class="table-light">
        <tr>
        <th>ID</th>
        <th>Username</th>
        <th>Email</th>
        <th>Specialization</th>
        <th>Department ID</th>
        <th>Actions</th>
        </tr>
      </thead>
    
      <tbody>
        
        <tr v-for="doc in doctors" :key="doc.id">

          <td>{{ doc.id }}</td>
          <td>{{ doc.username }}</td>
          <td>{{ doc.email }}</td>
          <td>{{ doc.specialization }}</td>
          <td>{{ doc.department_id }}</td>
          
          <td>
            <button class="btn btn-warning btn-sm" @click="$router.push(`/update-doctor/${doc.id}`)">
              Edit
            </button>
            <button class="btn btn-danger btn-sm" @click="deleteDoctor(doc.id)">Delete</button>
          </td>
          <td>
            <button class="btn btn-danger btn-sm" @click="blacklistUser(doc.user_id)">Blacklist</button>
          </td>
          

        </tr>

      </tbody>
    </table>

    <!-- paitent list -->
    <div class="card mt-4 p-3">

  
      <h4>Patients List</h4>
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in patients" :key="patient.id">
            <td>{{ patient.id }}</td>
            <td>{{ patient.username }}</td>
            <td>{{ patient.email }}</td>
            <td>
              <button class="btn btn-danger btn-sm" @click="blacklistUser(patient.user_id)">Blacklist</button>
            </td>
          </tr>
          <tr v-if="patients.length === 0">
            <td colspan="4" class="text-center">
              No patients found
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- doctor ko add karne ka form-->
    <div class="card mt-4 p-3">

      <h4>Add Doctor</h4>
      
      <form @submit.prevent="addDoctor">
        
        <input
        v-model="doctor.username"
        class="form-control mb-2"
        placeholder="Username"
        />
        
        <input
        v-model="doctor.email"
        class="form-control mb-2"
        placeholder="Email"
        />

        <input
        v-model="doctor.password"
        type="password"
        class="form-control mb-2"
          placeholder="Password"
          />

          <input
          v-model="doctor.specialization"
          class="form-control mb-2"
          placeholder="Specialization"
        />

        <input
          v-model="doctor.department_id"
          class="form-control mb-2"
          placeholder="Department ID"
        />

        
      <button type="submit" class="btn btn-success">Add Doctor</button>
      </form>

    </div>
    
    
    <!--doctorsList -->
    
    <div class="card mt-4 p-3">
        <button class="btn btn-danger" @click="logout">Logout</button>
    </div>   
  </div>

</template>


<script>
import API from "../services/api";

export default {
  data() {
    return {
      searchDoctor: "",
      searchPatient: "",
      doctors: [],
      patients:[],
      stats: {},
      doctor: {
        username: "",
        email: "",
        password: "",
        specialization: "",
        department_id: ""
      }
    };
  },

  methods: {

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push("/login")
    },
    async loadPatients() {
      try {
        const res = await API.get("/admin/patients")
        this.patients = res.data
      }
      catch(error) {
        console.error(error)
      }
    },
    async blacklistUser(id) {
      if (!confirm("Blacklist this user?")) return
      try {
        await API.put(`/admin/blacklist/${id}`)
        alert("User blacklisted")
        this.loadPatients()
        this.loadDoctors()
      }
      catch (error) {
        console.error(error)
      }
    },
    async loadDashboard() {
      const res = await API.get("/admin/dashboard");
      this.stats = res.data;
    },
    async loadDoctors() {

      const res = await API.get("/admin/doctors")

      this.doctors = res.data

    },
    async deleteDoctor(id){

      if(confirm("Delete doctor?")){

        await API.delete(`/admin/delete-doctors/${id}`)

        this.loadDoctors()

      }

    },
    async addDoctor() {

      try {

        const payload = {
          ...this.doctor,
          department_id: Number(this.doctor.department_id)
        }

        await API.post("/admin/doctors", payload)

        alert("Doctor added")

        this.doctor = {
          username: "",
          email: "",
          password: "",
          specialization: "",
          department_id: ""
        }

        await this.loadDoctors()
        await this.loadDashboard()

      }

      catch(error) {

        console.error(error)

      }

    },
    async searchDoctors() {
      if (!this.searchDoctor) {
        this.loadDoctors()
        return
      }
      const res = await API.get(`/admin/search/doctors?q=${this.searchDoctor}`)
      this.doctors = res.data
    },
    async searchPatients() {
      if (!this.searchPatient) {
        this.loadPatients()
        return
      }
      const res = await API.get(`/admin/search/patients?q=${this.searchPatient}`)
      this.patients = res.data
    }
  },

  mounted() {
    this.loadDashboard();
    this.loadDoctors();
    this.loadPatients();
  }

};
</script>