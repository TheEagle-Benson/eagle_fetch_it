def format_filesize(bytes_size: int|None) -> str:
    if bytes_size is None:
        return "Unknown size"
    
    units = ['B', 'KB', 'MB', 'GB']
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"

