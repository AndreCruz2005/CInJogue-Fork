import { useState } from "react";
export const backend: string = "http://127.0.0.1:5000";

export interface LoginProps {
	userData: any;
	setUserData: (data: any) => void;
}
