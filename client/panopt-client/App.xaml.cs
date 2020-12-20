using System.Windows;

namespace panopt_client
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App
    {
        private NetworkMonitor networkMonitor;
        private void OnStartup(object sender, StartupEventArgs eventArgs)
        {
            networkMonitor = NetworkMonitor.GetInstance();
            
            networkMonitor.StartService();
            // networkMonitor.ShowWindow();
        }
    }
}