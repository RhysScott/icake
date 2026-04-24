class ApiResponse: 
    @staticmethod 
    def success(data): 
        return {"success": True, "data": data} 
