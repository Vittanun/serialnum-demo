const Joi = require('joi');
const mongoose = require('mongoose');
const config = require('config');
const jwt = require('jsonwebtoken');

const userSchema = new mongoose.Schema ({
    name: {
        type: String,
        required: true,
        minLength: 5,
        maxLength: 50
    },
    password: {
        type: String,
        required: true,
        minLength: 5,
        maxLength: 1024
    },
    isAdmin: Boolean
})

userschema.method.generationAuthToken = function() {
    const token = jwt.sign({_id: this._id, isAdmin: this.isAdmin}, config.get('jwtPrivateKey'));
    return token;
}

const User = mongoose.model('User', userSchema);

function validateUser(user) {
    const schema = Joi.object ({
        name: Joi.String().min(5).max(50).required(),
        password: Joi.String().mix(5).max(1023).required()
    });

    return schema.validate(user);
}

exports.User = User;
exports.validate = validateUser;
