<template>
  <v-app>
    <RegisterHeader :logoImage="logoImage" />
    <v-main>
      <v-container class="py-10">
        <v-row>
          <!-- Left side: Image -->
          <v-col cols="12" md="6" class="d-flex align-center justify-center">
            <v-img
              :src="registerJobImage"
              alt="Registration Illustration"
              max-width="100%"
              max-height="600"
              contain
            ></v-img>
          </v-col>

          <!-- Right side: Form -->
          <v-col cols="12" md="6">
            <v-card class="elevation-4 fixed-card-height d-flex flex-column">
              <v-card-text class="flex-grow-1">
                <v-window v-model="currentStep" class="flex-grow-1">
                  <!-- Step 1: Personal Information -->
                  <v-window-item :value="1">
                    <v-form v-model="isStep1Valid">
                      <!-- Avatar upload -->
                      <div class="mb-8 text-center">
                        <v-avatar
                          size="120"
                          class="mb-4"
                          color="grey-lighten-2"
                          variant="outlined"
                        >
                          <v-img
                            v-if="formData.avatar"
                            :src="formData.avatar"
                          ></v-img>
                          <v-icon v-else size="48" color="grey"
                            >mdi-account</v-icon
                          >
                        </v-avatar>
                        <div class="position-relative">
                          <input
                            type="file"
                            ref="fileInput"
                            accept="image/*"
                            @change="handleFileUpload"
                            class="d-none"
                          />
                          <v-btn
                            size="small"
                            color="warning"
                            icon
                            class="position-absolute"
                            style="bottom: 0; right: 0"
                            @click="$refs.fileInput.click()"
                          >
                            <v-icon>mdi-plus</v-icon>
                          </v-btn>
                        </div>

                        <!-- Resume upload -->
                        <div class="mb-8 text-center">
                          <input
                            type="file"
                            ref="resumeInput"
                            accept=".pdf,.doc,.docx"
                            @change="handleResumeUpload"
                            class="d-none"
                          />
                          <v-btn
                            :loading="isParsingResume"
                            :disabled="isParsingResume"
                            color="primary"
                            @click="$refs.resumeInput.click()"
                            class="mb-4"
                          >
                            <v-icon start>mdi-file-upload</v-icon>
                            Upload Resume
                          </v-btn>
                          <div class="text-caption text-grey">
                            Supported formats: PDF, DOC, DOCX (Max 5MB)
                          </div>
                        </div>

                        <v-btn
                          block
                          color="primary"
                          class="mt-4"
                          :loading="isLoading"
                          :disabled="!selectedFile"
                          @click="extractResume"
                        >
                          Extract Information
                        </v-btn>
                      </div>

                      <!-- Personal Information Fields -->
                      <v-row>
                        <v-col cols="12" sm="6">
                          <h2 class="text-h6 mb-4">Firstname</h2>
                          <v-text-field
                            v-model="formData.firstName"
                            variant="outlined"
                            required
                            :rules="[(v) => !!v || 'First name is required']"
                            placeholder="Enter your first name"
                          ></v-text-field>
                        </v-col>

                        <v-col cols="12" sm="6">
                          <h2 class="text-h6 mb-4">Lastname</h2>
                          <v-text-field
                            v-model="formData.lastName"
                            variant="outlined"
                            required
                            :rules="[(v) => !!v || 'Last name is required']"
                            placeholder="Enter your last name"
                          ></v-text-field>
                        </v-col>

                        <v-col cols="12">
                          <h2 class="text-h6 mb-4">Email</h2>
                          <v-text-field variant="outlined"></v-text-field>
                        </v-col>

                        <v-col cols="12">
                          <v-row>
                            <v-col cols="9">
                              <h2 class="text-h6 mb-4">H/p</h2>
                              <v-text-field
                                v-model="formData.phoneNumber"
                                variant="outlined"
                                :placeholder="
                                  resumeData.phone || 'Enter your phone number'
                                "
                              ></v-text-field>
                            </v-col>
                          </v-row>
                        </v-col>
                      </v-row>
                    </v-form>
                  </v-window-item>

                  <!-- Step 2: Education -->
                  <!-- Step 2: Education -->
                  <v-window-item :value="2">
                    <v-form v-model="isStep2Valid">
                      <div class="mb-6">
                        <h2 class="text-h6 mb-4">Education</h2>
                        <v-row>
                          <v-col cols="12">
                            <!-- Display only the most recent education -->
                            <div
                              v-if="
                                resumeData.education &&
                                resumeData.education.length > 0
                              "
                            >
                              <v-list>
                                <v-list-item>
                                  <v-list-item-title>
                                    <strong>{{
                                      formatEducationInstitution(
                                        resumeData.education[0].university
                                      )
                                    }}</strong>
                                  </v-list-item-title>
                                  <v-list-item-subtitle>
                                    {{
                                      resumeData.education[0].degree || "Degree"
                                    }}
                                    in
                                    {{
                                      resumeData.education[0].major ||
                                      "Field of Study"
                                    }}
                                    ({{
                                      resumeData.education[0].graduationYear ||
                                      "Graduation Year"
                                    }})
                                  </v-list-item-subtitle>
                                </v-list-item>
                              </v-list>
                            </div>
                            <v-alert
                              v-else
                              type="info"
                              text="No education information found in resume"
                            ></v-alert>
                          </v-col>

                          <v-col cols="12">
                            <h2 class="text-h6 mb-4">Degree</h2>
                            <v-text-field
                              v-model="formData.degree"
                              variant="outlined"
                              :placeholder="
                                resumeData.education &&
                                resumeData.education.length > 0
                                  ? resumeData.education[0].degree || ''
                                  : 'Enter your degree'
                              "
                            ></v-text-field>
                          </v-col>

                          <v-col cols="12">
                            <h2 class="text-h6 mb-4">Field of study</h2>
                            <v-text-field
                              v-model="formData.major"
                              variant="outlined"
                              :placeholder="
                                resumeData.education &&
                                resumeData.education.length > 0
                                  ? resumeData.education[0].major || ''
                                  : 'Enter your field of study'
                              "
                            ></v-text-field>
                          </v-col>

                          <v-col cols="12">
                            <v-row>
                              <v-col cols="12" sm="6">
                                <h2 class="text-h6 mb-4">Graduation year</h2>
                                <v-text-field
                                  v-model="formData.graduationYear"
                                  variant="outlined"
                                  :placeholder="
                                    resumeData.education &&
                                    resumeData.education.length > 0
                                      ? resumeData.education[0]
                                          .graduationYear || ''
                                      : 'Enter your graduation year'
                                  "
                                ></v-text-field>
                              </v-col>

                              <v-col cols="12" sm="6">
                                <h2 class="text-h6 mb-4">CGPA</h2>
                                <v-text-field
                                  v-model="formData.gpa"
                                  variant="outlined"
                                  :rules="[
                                    (v) =>
                                      !v ||
                                      (!isNaN(parseFloat(v)) &&
                                        parseFloat(v) >= 0 &&
                                        parseFloat(v) <= 4.0) ||
                                      'CGPA must be a number between 0 and 4.0',
                                  ]"
                                  :placeholder="
                                    resumeData.education &&
                                    resumeData.education.length > 0
                                      ? resumeData.education[0].gpa || ''
                                      : 'Enter your CGPA (e.g., 3.5)'
                                  "
                                ></v-text-field>
                              </v-col>
                            </v-row>
                          </v-col>
                        </v-row>
                      </div>
                    </v-form>
                  </v-window-item>

                  <!-- Step 3: Skills -->
                  <v-window-item :value="3">
                    <v-form v-model="isStep3Valid">
                      <div class="mb-6">
                        <h2 class="text-h6 mb-4">Skills</h2>

                        <!-- Display skills as chips -->
                        <div
                          v-if="
                            resumeData.skills && resumeData.skills.length > 0
                          "
                          class="mb-4"
                        >
                          <h3 class="text-subtitle-1 mb-2">
                            Skills from your resume:
                          </h3>
                          <v-chip-group>
                            <v-chip
                              v-for="(skill, index) in resumeData.skills"
                              :key="index"
                              color="primary"
                              class="ma-1"
                              @click="addSkillToForm(skill)"
                            >
                              {{ skill }}
                            </v-chip>
                          </v-chip-group>
                          <div class="text-caption mt-2">
                            Click on a skill to add it to your profile
                          </div>
                        </div>

                        <!-- Skills input -->
                        <v-combobox
                          v-model="formData.skills"
                          label="Your Skills"
                          multiple
                          chips
                          variant="outlined"
                          hint="Enter your skills or select from above"
                          persistent-hint
                        ></v-combobox>
                      </div>
                    </v-form>
                  </v-window-item>

                  <!-- Step 4: Work Experience -->
                  <v-window-item :value="4">
                    <v-form v-model="isStep4Valid">
                      <v-switch
                        v-model="formData.isFreshGraduate"
                        label="I am a fresh graduate with no work experience"
                        class="mb-6"
                        color="primary"
                      ></v-switch>

                      <!-- Display extracted experience data -->
                      <div
                        v-if="
                          resumeData.experience &&
                          resumeData.experience.length > 0 &&
                          !formData.isFreshGraduate
                        "
                        class="mb-6"
                      >
                        <h3 class="text-subtitle-1 mb-2">
                          Experience from your resume:
                        </h3>
                        <v-expansion-panels>
                          <v-expansion-panel
                            v-for="(exp, index) in resumeData.experience"
                            :key="index"
                          >
                            <v-expansion-panel-title>
                              <strong>{{ exp.jobTitle || "Position" }}</strong>
                              at
                              {{ exp.company || "Company" }}
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                              <div>
                                <strong>Duration:</strong>
                                {{ formatDate(exp.startDate) || "Start date" }}
                                -
                                {{
                                  exp.endDate
                                    ? formatDate(exp.endDate)
                                    : "Present"
                                }}
                              </div>
                              <div class="mt-2">
                                <strong>Description:</strong>
                                {{
                                  exp.description || "No description available"
                                }}
                              </div>
                              <v-btn
                                color="primary"
                                class="mt-3"
                                @click="useExperienceFromResume(exp, index)"
                                variant="outlined"
                                size="small"
                              >
                                Use this experience
                              </v-btn>
                            </v-expansion-panel-text>
                          </v-expansion-panel>
                        </v-expansion-panels>
                      </div>

                      <div v-if="!formData.isFreshGraduate">
                        <div
                          v-for="(experience, index) in formData.experiences"
                          :key="index"
                          class="mb-6 pa-4 bg-grey-lighten-4 rounded-lg"
                        >
                          <div
                            class="d-flex justify-space-between align-center mb-4"
                          >
                            <h2 class="text-h6">
                              Work Experience {{ index + 1 }}
                            </h2>
                            <v-btn
                              v-if="index > 0"
                              icon="mdi-delete"
                              variant="text"
                              color="error"
                              @click="removeExperience(index)"
                            ></v-btn>
                          </div>

                          <v-text-field
                            v-model="experience.jobTitle"
                            label="Job Title"
                            variant="outlined"
                            required
                            :rules="[(v) => !!v || 'Job title is required']"
                          ></v-text-field>

                          <v-text-field
                            v-model="experience.company"
                            label="Company"
                            variant="outlined"
                            required
                            :rules="[(v) => !!v || 'Company name is required']"
                          ></v-text-field>

                          <v-row>
                            <v-col cols="6">
                              <v-menu
                                v-model="experience.startMenu"
                                :close-on-content-click="false"
                                transition="scale-transition"
                                min-width="auto"
                              >
                                <template v-slot:activator="{ props }">
                                  <v-text-field
                                    :model-value="
                                      formatDate(experience.startDate)
                                    "
                                    label="Start Date"
                                    variant="outlined"
                                    readonly
                                    v-bind="props"
                                    :rules="[
                                      dateRules.required,
                                      dateRules.notFuture,
                                    ]"
                                  ></v-text-field>
                                </template>
                                <v-date-picker
                                  v-model="experience.startDate"
                                  @update:model-value="
                                    experience.startMenu = false
                                  "
                                ></v-date-picker>
                              </v-menu>
                            </v-col>
                            <v-col cols="6">
                              <v-menu
                                v-model="experience.endMenu"
                                :close-on-content-click="false"
                                transition="scale-transition"
                                min-width="auto"
                              >
                                <template v-slot:activator="{ props }">
                                  <v-text-field
                                    :model-value="
                                      formatDate(experience.endDate)
                                    "
                                    label="End Date"
                                    variant="outlined"
                                    readonly
                                    v-bind="props"
                                    :rules="[
                                      dateRules.afterStart(
                                        experience.startDate
                                      ),
                                    ]"
                                    :disabled="experience.currentlyWorking"
                                  ></v-text-field>
                                </template>
                                <v-date-picker
                                  v-model="experience.endDate"
                                  @update:model-value="
                                    experience.endMenu = false
                                  "
                                  :min="experience.startDate"
                                ></v-date-picker>
                              </v-menu>
                            </v-col>
                          </v-row>

                          <v-switch
                            v-model="experience.currentlyWorking"
                            label="I am currently working here"
                            class="mb-4"
                            color="primary"
                            @change="
                              if (experience.currentlyWorking)
                                experience.endDate = null;
                            "
                          ></v-switch>

                          <v-textarea
                            v-model="experience.description"
                            label="Description"
                            variant="outlined"
                            rows="3"
                          ></v-textarea>
                        </div>

                        <v-btn
                          color="primary"
                          class="mb-6"
                          block
                          @click="addExperience"
                          v-if="!formData.isFreshGraduate"
                        >
                          Add Another Experience
                        </v-btn>
                      </div>
                    </v-form>
                  </v-window-item>
                </v-window>

                <!-- Progress indicator -->
                <div class="mt-8 mb-4">
                  <v-progress-linear
                    color="#366caa"
                    :model-value="progressValue"
                    height="8"
                    rounded
                  ></v-progress-linear>
                  <div class="text-caption text-end mt-1">
                    {{ currentStep }} of 4
                  </div>
                </div>
              </v-card-text>

              <!-- Navigation Buttons -->
              <v-card-actions>
                <v-row class="mt-6" no-gutters>
                  <v-col :cols="currentStep === 1 ? 12 : 6">
                    <v-btn
                      v-if="currentStep > 1"
                      color="primary"
                      variant="outlined"
                      block
                      @click="previousStep"
                    >
                      Back
                    </v-btn>
                  </v-col>
                  <v-col :cols="currentStep === 1 ? 12 : 6">
                    <v-btn
                      color="warning"
                      block
                      @click="currentStep === 4 ? submitForm() : nextStep()"
                      :disabled="!isCurrentStepValid"
                    >
                      {{ currentStep === 4 ? "Submit" : "Next" }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
// import RegisterHeader from "@/components/RegisterHeader.vue";
// import logoImage from "@/assets/jobified-name-transparent.png";
// import registerJobImage from "@/assets/registerjob.webp";

const router = useRouter();
const currentStep = ref(1);
const isStep1Valid = ref(false);
const isStep2Valid = ref(false);
const isStep3Valid = ref(false);
const isStep4Valid = computed(() => {
  if (formData.value.isFreshGraduate) {
    return true; // Skip validation if user is a fresh graduate
  }

  // Check if all experiences are valid
  return formData.value.experiences.every((exp) => {
    return (
      exp.jobTitle &&
      exp.company &&
      exp.startDate &&
      (exp.currentlyWorking || exp.endDate)
    );
  });
});

const selectedFile = ref(null);
const resumeData = ref({
  firstname: "",
  lastname: "",
  address: "",
  skills: [],
  experience: [],
  education: [],
});
const isLoading = ref(false);
const isParsingResume = ref(false);
const showError = ref(false);
const errorMessage = ref("");

const formData = ref({
  avatar: null,
  firstName: "",
  lastName: "",
  email: "",
  phoneNumber: "",
  university: [],
  degree: "",
  major: "",
  graduationYear: null,
  gpa: null,
  skills: [],
  isFreshGraduate: false,
  experiences: [
    {
      jobTitle: "",
      company: "",
      startDate: null,
      endDate: null,
      description: "",
      startMenu: false,
      endMenu: false,
      currentlyWorking: false,
    },
  ],
});

// Constants
const addSkillToForm = (skill) => {
  if (!formData.value.skills.includes(skill)) {
    formData.value.skills.push(skill);
  }
};

const yearsList = Array.from(
  { length: 10 },
  (_, i) => new Date().getFullYear() - i
);

const formatEducationInstitution = (institution) => {
  if (!institution) return "University";

  // Convert to lowercase for case-insensitive comparison
  const lowerInst = institution.toLowerCase();

  // Check for common abbreviations and variations
  if (
    lowerInst === "u" ||
    lowerInst === "uni" ||
    lowerInst === "univ" ||
    lowerInst.includes("university") ||
    lowerInst.includes("universiti") ||
    lowerInst.includes("college") ||
    lowerInst.includes("institute") ||
    lowerInst.includes("school")
  ) {
    // If it's a recognized abbreviation, return the original with proper formatting
    return institution.charAt(0).toUpperCase() + institution.slice(1);
  }

  // For other cases, check if it might be an abbreviation (short text)
  if (institution.length <= 5) {
    // It might be an abbreviation, try to expand it
    if (lowerInst.includes("u")) {
      return institution.toUpperCase() + " University";
    }
    // Add more abbreviation expansions as needed
  }

  // If nothing matches, return the original with proper formatting
  return institution.charAt(0).toUpperCase() + institution.slice(1);
};

const gpaScale = Array.from({ length: 41 }, (_, i) => (i / 10).toFixed(1));

// Validation rules

const dateRules = {
  required: (v) => !!v || "Date is required",
  notFuture: (v) => {
    if (!v) return true;
    const selectedDate = new Date(v);
    const today = new Date();
    return selectedDate <= today || "Date cannot be in the future";
  },
  afterStart: (startDate) => (v) => {
    if (!v || !startDate) return true;
    const start = new Date(startDate);
    const end = new Date(v);
    return end >= start || "End date must be after start date";
  },
};

// Computed properties
const progressValue = computed(() => (currentStep.value / 4) * 100);

const isCurrentStepValid = computed(() => {
  switch (currentStep.value) {
    case 1:
      return isStep1Valid.value;
    case 2:
      return isStep2Valid.value;
    case 3:
      return isStep3Valid.value;
    case 4:
      return formData.value.isFreshGraduate || isStep4Valid.value;
    default:
      return false;
  }
});

// Methods
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      formData.value.avatar = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleResumeUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "";

  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString; // If not a valid date, return as is

    return date.toLocaleDateString("en-GB", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  } catch (e) {
    console.error("Error formatting date:", e);
    return dateString; // Return original string if there's an error
  }
};

const addExperience = () => {
  formData.value.experiences.push({
    jobTitle: "",
    company: "",
    startDate: null,
    endDate: null,
    description: "",
    startMenu: false,
    endMenu: false,
    currentlyWorking: false,
  });
};

const removeExperience = (index) => {
  formData.value.experiences.splice(index, 1);
};

const nextStep = () => {
  if (isCurrentStepValid.value && currentStep.value < 4) {
    currentStep.value++;
  }
};

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const submitForm = () => {
  if (formData.value.isFreshGraduate || isStep4Valid.value) {
    console.log("Form submitted:", formData.value);
    router.push("/jobseeker/dashboard");
  }
};

const extractResume = async () => {
  if (!selectedFile.value) {
    errorMessage.value = "Please upload a resume file.";
    showError.value = true;
    return;
  }

  isLoading.value = true;
  showError.value = false;

  try {
    const formDataObj = new FormData();
    formDataObj.append("file", selectedFile.value);

    const response = await fetch("http://localhost:8000/summarize_resume", {
      method: "POST",
      body: formDataObj,
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to process resume");
    }

    const data = await response.json();
    resumeData.value = data;

    // Automatically populate form fields with extracted data
    if (data.firstname) formData.value.firstName = data.firstname;
    if (data.lastname) formData.value.lastName = data.lastname;
    if (data.email) formData.value.email = data.email;
    if (data.phone) formData.value.phoneNumber = data.phone;

    // Only set skills if they exist and formData.skills is empty
    if (
      data.skills &&
      data.skills.length > 0 &&
      formData.value.skills.length === 0
    ) {
      formData.value.skills = [...data.skills];
    }

    // Map education data
    if (data.education && data.education.length > 0) {
      const education = data.education[0]; // Use the first education entry
      if (education.university)
        formData.value.university = education.university;
      if (education.degree) formData.value.degree = education.degree;
      if (education.major) formData.value.major = education.major;
      if (education.graduationYear)
        formData.value.graduationYear = education.graduationYear;
      if (education.gpa) formData.value.gpa = education.gpa;
    }

    // Map experience data - but don't overwrite the form data if user has already entered something
    if (
      data.experience &&
      data.experience.length > 0 &&
      !formData.value.experiences[0].jobTitle &&
      !formData.value.experiences[0].company
    ) {
      // Initialize with the first experience
      formData.value.experiences[0] = {
        jobTitle: data.experience[0].jobTitle || "",
        company: data.experience[0].company || "",
        startDate: data.experience[0].startDate || null,
        endDate: data.experience[0].endDate || null,
        description: data.experience[0].description || "",
        startMenu: false,
        endMenu: false,
        currentlyWorking: !data.experience[0].endDate,
      };
    }

    // Optional: Show a simple success message
    alert("Resume data extracted successfully!");
  } catch (error) {
    errorMessage.value =
      error.message || "An error occurred while processing the resume.";
    showError.value = true;
  } finally {
    isLoading.value = false;
  }
};

const useExperienceFromResume = (exp, index) => {
  console.log("Using experience:", exp); // Add this for debugging

  // If we need to create a new experience slot
  while (index >= formData.value.experiences.length) {
    addExperience();
  }

  // Make sure dates are in the correct format
  let startDate = null;
  let endDate = null;

  // Try to parse dates if they exist
  if (exp.startDate) {
    try {
      startDate = exp.startDate;
      // If it's not already a date string in YYYY-MM-DD format, try to convert it
      if (!startDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const date = new Date(startDate);
        if (!isNaN(date.getTime())) {
          startDate = date.toISOString().split("T")[0];
        }
      }
    } catch (e) {
      console.error("Error parsing start date:", e);
    }
  }

  if (exp.endDate) {
    try {
      endDate = exp.endDate;
      // If it's not already a date string in YYYY-MM-DD format, try to convert it
      if (!endDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const date = new Date(endDate);
        if (!isNaN(date.getTime())) {
          endDate = date.toISOString().split("T")[0];
        }
      }
    } catch (e) {
      console.error("Error parsing end date:", e);
    }
  }

  // Update the experience data with explicit property assignment
  formData.value.experiences[index].jobTitle = exp.jobTitle || "";
  formData.value.experiences[index].company = exp.company || "";
  formData.value.experiences[index].startDate = startDate;
  formData.value.experiences[index].endDate = endDate;
  formData.value.experiences[index].description = exp.description || "";
  formData.value.experiences[index].startMenu = false;
  formData.value.experiences[index].endMenu = false;
  formData.value.experiences[index].currentlyWorking = !endDate;

  // Force a UI update
  formData.value = { ...formData.value };

  // Show a success message
  alert(
    `Experience "${exp.jobTitle} at ${exp.company}" has been added to your form.`
  );
};
</script>

<style scoped>
.fixed-card-height {
  min-height: 900px;
}

.position-relative {
  position: relative;
}

.position-absolute {
  position: absolute;
}
</style>
