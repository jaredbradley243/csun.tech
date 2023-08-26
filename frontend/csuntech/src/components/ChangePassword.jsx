import React from 'react';
import './ChangePassword.css';

function ChangePassword() {
    return (
        <div className="accountsettings">
            <h1 className="main-header">Change Password</h1>

            <div className="settings-form">
                <div className="form-group">
                    <label htmlFor="oldPass">
                        Old Password <span>*</span>
                    </label>
                    <input type="password" name="oldPass" id="oldPass" />
                </div>

                <div className="form-group">
                    <label htmlFor="newPass">
                        New Password <span>*</span>
                    </label>
                    <input type="password" name="newPass" id="newPass" />
                </div>

                <div className="form-group">
                    <label htmlFor="confirmPass">
                        Confirm Password <span>*</span>
                    </label>
                    <input
                        type="password"
                        name="confirmPass"
                        id="confirmPass"
                    />
                </div>
            </div>
            <button className="saveBtn" type="submit">
                Save Changes
            </button>
        </div>
    );
}

export default ChangePassword;
