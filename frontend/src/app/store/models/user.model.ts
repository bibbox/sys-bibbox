export interface UserRepresentation {
  id: string;
  username: string;
  roles: string[];
  firstName?: string;
  lastName?: string;
  email?: string;
}

export interface RoleRepresentation {
  id?: string;
  name?: string;
  description?: string;
  scopeParamRequired?: boolean;
  composite?: boolean;
  clientRole?: boolean;
  containerId?: string;
}

export interface UserDictionary {
  username: string;
  password?: string;
  roles: string[];
  email?: string;
  firstName?: string;
  lastName?: string;
}

export interface UserRoleMapping {
  user_role_mappings: UserRoles[];
}

export interface UserRoles {
  user_id: string;
  roles: string[];
}

export interface CreateUserSuccessResponse {
  message: string;
  userRepresentation: UserRepresentation;
}

export interface UpdateRoleMappingSuccessResponse {
  message: string;
  users: UserRepresentation[];
}

export interface DeleteUserSuccessResponse {
  message: string;
  userID: string;
}

export interface UserCreateDialogProps {
  usernames: string[];
  userToEdit: UserRepresentation | null;
}


// export interface UserRepresentation {
//   id?: string;
//   createdTimestamp?: number;
//   username?: string;
//   firstName?: string;
//   lastName?: string;
//   email?: string;
//   enabled?: boolean;
//   emailVerified?: boolean;
//   totp?: boolean;
//   access?: Record<string, boolean>;
//   attributes?: Record<string, any>;
//   disableableCredentialTypes?: string[];
//   requiredActions?: string[];
//   notBefore?: number;
//   federationLink?: string;
//   clientRoles?: Record<string, string[]>;
//   realmRoles?: string[];
//   credentials?: CredentialRepresentation[];
//   groups?: GroupRepresentation[];
// }

// export interface GroupRepresentation {
//   id?: string;
//   name?: string;
//   path?: string;
//   subGroups?: GroupRepresentation[];
//   access?: Record<string, boolean>;
//   attributes?: Record<string, any>;
// }
//
// interface CredentialRepresentation {
//   type?: string;
//   value?: string;
//   temporary?: boolean;
//   createdDate?: number;
//   salt?: string;
//   hashIterations?: number;
//   counter?: number;
//   algorithm?: string;
//   config?: Record<string, any>;
// }
