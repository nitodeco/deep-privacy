from agent import generate_privacy_report


def main():
    print("🔒 Deep Privacy CLI")
    print("Create privacy reports for online services.\n")

    service = input("Enter service name (e.g. Spotify, Notion): ").strip()

    if not service:
        print("Error: Service name cannot be empty")
        return

    print(f"\nGenerating privacy report for {service}...")
    generate_privacy_report(service)


if __name__ == "__main__":
    main()
