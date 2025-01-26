import mongoose from "mongoose";

const profileSchema = new mongoose.Schema({
    age: {
        type: String,
    },
    bloodPressure: {
        type:String,
    },
    insulinLevel: {
        type: String,
        
    },
    BMI: {
        type: String,
    },
    diabetesPedigreeFunction: {
        type: String,
    },
    bloodGlucose: {
        type: String,
    },
    pregnancies: {
        type: String
    },
    diabetesVersion: {
        type: Number
    },
    skinThickness : {
        type: String
    }
})

const User = mongoose.models.User || mongoose.model("User", profileSchema)

export default User
