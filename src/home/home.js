import { DTO } from "../js/dto.js";

import { user } from "../js/session.js";

// wip, mas vai puxar a info do banco de dados
class Home {
  static async getDashboardData() {
    return DTO.findPaciente({ id: user.DTO.id });
  }
}