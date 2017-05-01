<html>
<body>
<form runat="server">
<asp:TextBox ID="op1" RunAt="server" />
+
<asp:TextBox ID="op2" RunAt="server" />
<asp:Button Text=" = "OnClick="OnAdd" RunAt="server" />
<asp:Label ID="Sum" RunAt="server" />
</form>
</body>
</html>
<script language="C#" runat="server">
void OnAdd (Object sender, EventArgs e)
{
int a = Convert.ToInt32 (op1.Text);
int b = Convert.ToInt32 (op2.Text);
Sum.Text = (a + b).ToString ();
}
</script> 
