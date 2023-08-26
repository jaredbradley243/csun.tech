/* eslint-disable prettier/prettier */
import React from 'react';
import './AccountSettings.css';

export default function AccountSettings() {
    return (
        <div className="accountsettings">
            <h1 className="main-header">Personal Information</h1>

            <div className="settings-form">
                <div className="form-group">
                    <label htmlFor="firstName">
                        First Name <span>*</span>
                    </label>
                    <input type="text" name="firstName" id="firstName" />
                </div>

                <div className="form-group">
                    <label htmlFor="lastName">
                        Last Name <span>*</span>
                    </label>
                    <input type="text" name="lastName" id="lastName" />
                </div>

                <div className="form-group">
                    <label htmlFor="email">
                        Email <span>*</span>
                    </label>
                    <input type="email" name="email" id="email" />
                </div>
            </div>
            <button className="saveBtn" type="submit">
                Save Changes
            </button>
        </div>
    );
}
